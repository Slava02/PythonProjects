import os
import markdown
from http.server import HTTPServer, BaseHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader
import mimetypes
import subprocess
import time

CONTENT_DIR = 'content'
POST_DIR = 'posts'
TEMPLATES_DIR = 'templates'
STATIC_DIR = 'static'

env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))


def get_go(path_to_go, script_folder='./scripts/'):
    try:
        proc = subprocess.Popen(script_folder+path_to_go, shell=True, stdout=subprocess.PIPE)
        if proc.returncode:
            return f"<pre style='color:red;'>Error: {proc.stderr.read().decode()}</pre>"
        return f"<pre>{proc.stdout.read().decode()}</pre>"
    except Exception as e:
        return f"<pre style='color:red;'>Exception: {str(e)}</pre>"

def get_php(path_to_php, script_folder='./scripts/'):
    try:
        proc = subprocess.Popen(["php", script_folder+path_to_php], shell=True, stdout=subprocess.PIPE)
        if proc.returncode:
            return f"<pre style='color:red;'>Error: {proc.stderr.read().decode()}</pre>"
        return f"<pre>{proc.stdout.read().decode()}</pre>"
    except Exception as e:
        return f"<pre style='color:red;'>Exception: {str(e)}</pre>"

def get_post(post_path):
    with open(post_path, 'r', encoding='utf-8') as file:
        content = file.read()

    lines = content.split('\n')
    title = lines[0].strip('# ')

    html_content = markdown.markdown(content)
    html_content = html_content.replace('../imgs/', '/imgs/')

    return {'content': html_content, 'title': title}


def get_all_posts():
    posts = []
    posts_dir = os.path.join(CONTENT_DIR, POST_DIR)
    for filename in os.listdir(posts_dir):
        if filename.endswith('.md'):
            post_path = os.path.join(posts_dir, filename)
            post = get_post(post_path)
            if post:
                post['url'] = f'/posts/{filename[:-3]}/'
                posts.append(post)
    return posts


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            posts = get_all_posts()
            template = env.get_template('posts.html')
            html = template.render(posts=posts, title='All Posts')
            self.wfile.write(html.encode())

        elif self.path.startswith('/posts/'):
            post_name = self.path.split('/')[-2]
            post_path = os.path.join(CONTENT_DIR, POST_DIR, f'{post_name}.md')
            if os.path.exists(post_path):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                post = get_post(post_path)
                template = env.get_template('post.html')
                html = template.render(post=post)
                self.wfile.write(html.encode())
            else:
                self.send_error(404, 'Post not found')

        elif self.path.startswith('/static/'):
            try:
                with open(self.path[1:], 'rb') as file:
                    self.send_response(200)
                    if self.path.endswith('.css'):
                        self.send_header('Content-type', 'text/css')
                    elif self.path.endswith('.js'):
                        self.send_header('Content-type', 'application/javascript')
                    self.end_headers()
                    self.wfile.write(file.read())
            except FileNotFoundError:
                self.send_error(404, 'File not found')

        elif self.path.startswith('/imgs/'):
            try:
                img_path = os.path.join(CONTENT_DIR, self.path[1:])
                mime_type, _ = mimetypes.guess_type(img_path)

                with open(img_path, 'rb') as file:
                    self.send_response(200)
                    self.send_header('Content-type', mime_type or 'application/octet-stream')
                    self.end_headers()
                    self.wfile.write(file.read())

            except FileNotFoundError:
                self.send_error(404, 'Image not found')

        elif self.path.startswith('/exe/'):
            try:
                path = self.path.split('/')
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                template = env.get_template('script.html')
                html = template.render(script_message=get_go(path[2]))
                self.wfile.write(html.encode())
            except FileNotFoundError:
                self.send_error(404, 'Go file not found')

        elif self.path.startswith('/php/'):
            try:
                path = self.path.split('/')
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                template = env.get_template('script.html')
                html = template.render(script_message=get_php(path[2]))
                self.wfile.write(html.encode())
            except FileNotFoundError:
                self.send_error(404, 'Go file not found')

        else:
            self.send_error(404, 'Page not found')


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'http://localhost:{port}')
    httpd.serve_forever()


if __name__ == "__main__":
    run()
