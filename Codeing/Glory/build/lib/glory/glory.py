import argparse
import paramiko
import sqlite3
import os
import getpass
from pathlib import Path

class GlorySSH:
    def __init__(self):
        self.db_path = os.path.join(str(Path.home()), '.glory.db')
        self.init_database()

    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS servers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                label TEXT NOT NULL UNIQUE
            )
        ''')
        conn.commit()
        conn.close()

    def add_new_server(self):
        """添加新的服务器配置"""
        ip = input("请输入服务器IP地址: ")
        username = input("请输入用户名: ")
        password = getpass.getpass("请输入密码: ")
        label = input("请输入标签: ")

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO servers (ip, username, password, label)
                VALUES (?, ?, ?, ?)
            ''', (ip, username, password, label))
            conn.commit()
            print(f"成功添加服务器配置，标签为: {label}")
        except sqlite3.IntegrityError:
            print("错误：标签已存在")
        finally:
            conn.close()

    def connect_server(self, label):
        """通过标签连接服务器"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT ip, username, password FROM servers WHERE label = ?', (label,))
        server = cursor.fetchone()
        conn.close()

        if not server:
            print(f"未找到标签为 {label} 的服务器配置")
            return

        ip, username, password = server
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, username=username, password=password)
            print("太棒了喵！\n")
            print(f"成功连接到 {ip}:{label}")
            
            # 创建交互式shell会话
            channel = ssh.invoke_shell()
            while True:
                if channel.recv_ready():
                    output = channel.recv(4096).decode('utf-8')
                    print(output, end='')
                try:
                    command = input("")
                    if command.lower() == 'exit':
                        break
                    channel.send(command + "\n")
                except EOFError:
                    break
            
            ssh.close()
            print("连接已关闭")
        except Exception as e:
            print(f"连接失败: {str(e)}")

def list_servers():
    """列出所有保存的服务器配置"""
    config = load_config()
    if not config:
        print("没有保存的服务器配置")
        return
    
    print("\n当前保存的服务器列表：")
    print("-" * 50)
    print(f"{'标签名':<15}{'用户名':<15}{'主机地址':<20}")
    print("-" * 50)
    for label, info in config.items():
        print(f"{label:<15}{info['username']:<15}{info['hostname']:<20}")
    print("-" * 50)

def main():
    parser = argparse.ArgumentParser(description='SSH连接管理工具')
    parser.add_argument('-n', '--new', action='store_true', help='添加新的服务器配置')
    parser.add_argument('-c', '--connect', metavar='LABEL', help='连接到指定标签的服务器')
    parser.add_argument('-l', '--list', action='store_true', help='列出所有保存的服务器')
    
    args = parser.parse_args()
    
    if args.new:
        add_new_server()
    elif args.connect:
        connect_server(args.connect)
    elif args.list:
        list_servers()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
