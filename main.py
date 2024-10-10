from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)



def generate_maze(n, m):
    maze = [[random.choice([0, 1]) for i in range(m)] for i in range(n)]
    maze[0][0] = 0
    maze[n - 1][m - 1] = 0
    return maze


def find_path(maze, x, y, path):
    n = len(maze)
    m = len(maze[0])

    if x == n - 1 and y == m - 1:
        path.append((x, y))
        return True

    if x >= 0 and y >= 0 and x < n and y < m and maze[x][y] == 0:
        path.append((x, y))
        maze[x][y] = 2

        if find_path(maze, x + 1, y, path):
            return True
        if find_path(maze, x, y + 1, path):
            return True
        if find_path(maze, x - 1, y, path):
            return True
        if find_path(maze, x, y - 1, path):
            return True

        path.pop()
        return False

    return False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_maze/<int:n>/<int:m>')
def generate(n, m):
    maze = generate_maze(n, m)
    return jsonify({"maze": maze})


@app.route('/solve_maze', methods=['POST'])
def solve():
    maze = request.json.get('maze')
    path = []
    if find_path(maze, 0, 0, path):
        return jsonify({"path": path})
    else:
        return jsonify({"path": None})


if __name__ == '__main__':
    app.run(debug=True, port=1488)

