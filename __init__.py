from flask import Flask
app = Flask(__name__)

cheerfile = "/dev/shm/cheer.txt"

@app.route('/')
def read_cheer():
    try:
        f = open(cheerfile, 'r')
        cheer = f.read()
        f.close()
    except IOError:
        cheer = write_cheer(0)
    return cheer

@app.route('/<int:cheer>')
def write_cheer(cheer):
    if cheer < 1000:
        cheer = "%.3d"%(cheer)
        f = open(cheerfile,'w+')
        f.seek(0)
        f.write(cheer)
        f.truncate()
        f.close()
    else:
        cheer = "Invalid Value Ignored"
    return cheer

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
