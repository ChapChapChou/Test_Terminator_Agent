from flask import Flask, render_template
from flask_socketio import SocketIO
import os
import sys
import io
from test_generator_agent import TestGeneratorAgent
import threading
import time
import re
from contextlib import redirect_stdout

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# 禁用Flask的自动重载功能
app.config['TEMPLATES_AUTO_RELOAD'] = False

@app.route('/')
def index():
    return render_template('index.html')

class OutputCapture:
    def __init__(self):
        self.buffer = io.StringIO()
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr

    def __enter__(self):
        sys.stdout = self
        sys.stderr = self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr

    def write(self, data):
        # 写入原始 stdout/stderr (用于服务器终端)
        self.old_stdout.write(data)
        # 可选：在缓冲区中存储原始数据
        self.buffer.write(data)

        # *** 重要：直接发送原始数据 ***
        # cleaned_data = self.ANSI_ESCAPE_PATTERN.sub('', data) # 删除这一行
        if data: # 确保不发送空字符串
             # 全局引用 socketio 实例 (或者通过参数传入)
             socketio.emit('message', {'type': 'output', 'content': data}) # 发送原始 data

    def flush(self):
        self.buffer.flush()
        self.old_stdout.flush()

@socketio.on('start_generation')
def handle_generation(data):
    source_dir = data.get('source_dir', '')
    
    if not source_dir:
        socketio.emit('message', {'type': 'error', 'content': 'Please provide a source directory path'})
        return
    
    if not os.path.exists(source_dir):
        socketio.emit('message', {'type': 'error', 'content': f'Directory not found: {source_dir}'})
        return
    
    # 创建一个新的线程来运行测试生成过程
    def run_test_generation():
        try:
            # 发送开始消息
            socketio.emit('message', {'type': 'agent', 'content': f'Starting test generation for directory: {source_dir}'})
            
            # 创建一个自定义的TestGeneratorAgent，它会发送消息到前端
            agent = TestGeneratorAgent()
            
            # 使用OutputCapture来捕获所有输出
            with OutputCapture():
                # 运行测试生成过程
                result = agent.run(source_dir)
            
            # 发送完成消息
            socketio.emit('message', {'type': 'success', 'content': 'Test generation completed successfully!'})
            
        except Exception as e:
            # 发送错误消息
            socketio.emit('message', {'type': 'error', 'content': f'Error during test generation: {str(e)}'})
            import traceback
            print(f"Error traceback: {traceback.format_exc()}")
    
    # 启动线程
    thread = threading.Thread(target=run_test_generation)
    thread.daemon = True
    thread.start()

if __name__ == '__main__':
    # 禁用Flask的自动重载功能
    socketio.run(app, debug=False, port=3000) 