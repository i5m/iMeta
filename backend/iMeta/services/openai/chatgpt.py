import openai
import os


class ChatGPTWrapper:

    def __init__(self):
        openai.api_key = os.environ.get("OPENAI_API_KEY")

    def organise(self, query):

        response = openai.ChatCompletion.create(
            # model="gpt-3.5-turbo",
            model="gpt-3.5-turbo-16k",
            messages = [
                {"role": "system", "content": "Act as a helpful and fantastic content organiser who excels in extracting valuable insights from the given unstructed html text contents."},
                {"role": "user", "content": query},
                {"role": "user", "content": "Understand these contents and write down most important aggregated bullet points that can be extracted from this. If you wish you can also structure content with headings such as about, latest news, links, etc, where each heading will contain few relevant bullets whenever necessary. Only write the main answer and nothing else."}
            ]
        )

        return response


    def get_keyword(self, q):

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages = [
                {"role": "system", "content": "Act as a complicated neural NLP model. Your task is to extract the most relevant keyword from the user's search query. The keyword could be anything such as name, place, object, noun, etc. Please write the answer in the format - Keyword: {answer}."},
                {"role": "user", "content": q}
            ]
        )

        return response


    def get_map(self, conn, res):

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages = [
                {"role": "system", "content": '''Act as a mind map flowchart designer who ideates at the speed of thought, generate new concepts and break through mental blocks with the given content. Your task is to suggest 3-5 very concise ideas based on pervious map connection and new content.

Format: Each bullet should contain only a few keywords which is very relevant to the content insights and do not write anything else. After every bullet, write a string </abc>.

For reference, the ideas or keywords from the content could be places, persons, things to do, sections of blogs, how-to's, research options, follow ups, etc.'''},

                {"role": "user", "content": f'''
Map Connection: {conn},

Results:
{res}
'''}

            ]
        )

        return response

