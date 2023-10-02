from flask import request, abort, jsonify
from iMeta.services.metaphor import MetaphorWrapper
from iMeta.services.openai.chatgpt import ChatGPTWrapper
from iMeta.services.wikimedia import WikiImagesWrapper
from iMeta.services.transformers.blip import ImageInfoWrapper


def new_search():

    # response = jsonify({
    #     "data": {
    #         "content": "Bill Gates bullet points:\n- Full Name: William Henry Gates III\n- Date of Birth: October 28, 1955\n- Nationality: American\n- Occupation: Businessman, investor, philanthropist, programmer, writer\n- Known for: Co-founding Microsoft and Bill & Melinda Gates Foundation\n- Spouse(s): Melinda French (married in 1994, divorced in 2021)\n- Children: 3\n- Parents: Bill Gates Sr. (father) and Mary Maxwell Gates (mother)\n- Education: Dropped out of Harvard University\n- Awards: Knight Commander of the Order of the British Empire, Padma Bhushan, Presidential Medal of Freedom, Hilal-e-Pakistan\n- Current roles: Co-chair of the Bill & Melinda Gates Foundation, Chairman and founder of Cascade Investment and Branded Entertainment Network, Chairman and co-founder of TerraPower, Founder of Breakthrough Energy and Gates Ventures, Technology advisor of Microsoft\n- Career highlights: Co-founded Microsoft with Paul Allen, held various positions at Microsoft including chairman, CEO, president, and chief software architect, led the microcomputer revolution in the 1970s and 1980s\n- Philanthropic efforts: Co-founded the Bill & Melinda Gates Foundation, donated sizable amounts to various charitable organizations and scientific research programs, led a vaccination campaign that contributed to the eradication of poliovirus in Africa\n- Wealth: Included in Forbes list of world's billionaires since 1987, consistently ranked as one of the richest people in the world\n\nNote: The extracted information is based on the available text and may not include every detail about Bill Gates.",
    #         "images": [
    #             "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Bill_Gates_2017_%28cropped%29.jpg/50px-Bill_Gates_2017_%28cropped%29.jpg",
    #             "https://upload.wikimedia.org/wikipedia/commons/1/1e/170217-D-GO396-0147_%2832577063650%29.jpg",
    #             "https://upload.wikimedia.org/wikipedia/commons/0/01/Altair_8800_Computer.jpg",
    #             "https://upload.wikimedia.org/wikipedia/commons/2/23/Berkshire_Hathaway.svg",
    #             "https://upload.wikimedia.org/wikipedia/commons/e/ea/Bill_Gates_-_World_Economic_Forum_Annual_Meeting_Davos_2008.jpg",
    #             "https://upload.wikimedia.org/wikipedia/commons/a/a8/Bill_Gates_2017_%28cropped%29.jpg",
    #             "https://upload.wikimedia.org/wikipedia/commons/1/19/Bill_Gates_June_2015.jpg",
    #             "https://upload.wikimedia.org/wikipedia/commons/8/84/Bill_Gates_at_Singapore_FinTech_Festival_2020.jpg",
    #             "https://upload.wikimedia.org/wikipedia/commons/3/34/Bill_Gates_signature.svg",
    #             "https://upload.wikimedia.org/wikipedia/commons/2/28/Bill_og_Melinda_Gates_2009-06-03_%28bilde_01%29.JPG"
    #         ],
    #         "keyword": " Bill Gates"
    #     }
    # })

    # response.headers.add("Access-Control-Allow-Origin", "*")
    # response.headers.add("Access-Control-Allow-Headers", "*")
    # response.headers.add("Access-Control-Allow-Methods", "*")

    # return response

    try:
        q = request.args.get('q').strip()
    except:
        abort(403)

    mw = MetaphorWrapper()
    cg = ChatGPTWrapper()
    wiki_img = WikiImagesWrapper()
    
    results = mw.search(q)
    ids = [i.id for i in results]

    if len(ids) < 0:
        abort(401)

    contents = mw.get_content(ids)
    contents_str = f"Orginal Query: {q}\n\nResults:\n\n"
    for i in contents:
        contents_str += f'''
{"#" * 20}

Title: {i.title}

Content:
{i.extract}
'''
        
        if len(contents_str) > 16385:
            contents_str = contents_str[:16384]
            break
    
    cg_info = cg.organise(contents_str)

    cg_key = cg.get_keyword(q)
    cg_key = cg_key['choices'][0]['message']['content'].replace('Keyword:', '')

    images = wiki_img.get_images(cg_key)

    response = jsonify({
        "data": {
            "content": cg_info['choices'][0]['message']['content'],
            "keyword": cg_key,
            "images": images
        }
    })

    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")

    return response



def mind_map():

    try:
        q = request.form.get('q').strip()
        history = request.form.get('history').split(',')
    except:
        abort(401)

    mw = MetaphorWrapper()
    cg = ChatGPTWrapper()

    cg_key = cg.get_keyword(q)
    cg_key = cg_key['choices'][0]['message']['content'].replace('Keyword:', '')

    results = mw.search(
        cg_key + ' '.join(history[::-1])
    )
    ids = [i.id for i in results]

    if len(ids) < 0:
        abort(401)

    contents = mw.get_content(ids)
    contents_str = ''
    for i in contents:
        contents_str += f'''
{"#" * 20}

Title: {i.title}

Content:
{i.extract}
'''
        
        if len(contents_str) > 16385:
            contents_str = contents_str[:16384]
            break

    ans = cg.get_map(
        ' -> '.join(history) + ' -> ' + cg_key,
        contents_str
    )

    response = jsonify({
        "data": {
            "content": ans['choices'][0]['message']['content'],
            "keyword": cg_key
        }
    })

    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")

    return response


def image_search():

    imagefile = request.files.get('imagefile', '')

    if imagefile == '':
        abort(403)

    img_info = ImageInfoWrapper()
    cg = ChatGPTWrapper()

    answer = img_info.get_image_info(imagefile)
    keyword = cg.get_keyword(answer[0]["generated_text"])
    keyword = keyword['choices'][0]['message']['content'].replace('Keyword:', '')

    response = jsonify({
        "data": {
            "answer": answer,
            "keyword": keyword
        }
    })

    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")

    return response

