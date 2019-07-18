from flask import Flask, request

app = Flask(__name__)

german_to_english = {
    'halo' : 'hello',
    'kalt' : 'cold'
}


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/translate_to_english', methods=['GET'])
def translate_to_english():
    german_word = request.json['german_word']
    try:
        return german_to_english[german_word]
    except KeyError as ex:
        return f'{german_word} is not a valid/available word'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)