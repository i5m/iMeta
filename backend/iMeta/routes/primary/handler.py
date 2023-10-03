from flask import request, abort, jsonify
from iMeta.services.metaphor import MetaphorWrapper
from iMeta.services.openai.chatgpt import ChatGPTWrapper
from iMeta.services.wikimedia import WikiImagesWrapper
from iMeta.services.transformers.blip import ImageInfoWrapper


def new_search():

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

