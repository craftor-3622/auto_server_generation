import sys
import re
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget

class ServerWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    # UI 초기화
    def initUI(self):
        # 버튼 정의
        startBtn = QPushButton('서버 실행', self)
        startBtn.setToolTip('버튼을 눌러 서버를 실행합니다.')
        
        breakBtn = QPushButton('서버 중단', self)
        breakBtn.setToolTip('버튼을 눌러 서버를 중단합니다.')

        quitBtn = QPushButton('닫기', self)
        quitBtn.setToolTip('버튼을 눌러 프로그램을 종료합니다.')

        grid = QGridLayout()
        self.setLayout(grid)
        grid.setSpacing(10)
        grid.addWidget(startBtn, 0, 0)
        grid.addWidget(breakBtn, 1, 0)
        grid.addWidget(quitBtn, 2, 0)
        
        startBtn.clicked.connect(self.start_server)
        breakBtn.clicked.connect(self.stop_server)
        quitBtn.clicked.connect(self.close)
        

        self.setWindowTitle('FastAPI Server Console')
        self.resize(400, 200)
        self.center()
        self.show()

    # 창을 화면 중앙으로 위치
    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def start_server(self):
        subprocess.Popen('uvicorn main:app --reload', shell=True)

    def stop_server(self, port=8000):
        try:
            # 포트를 사용하는 PID 조회
            result = subprocess.check_output(f'netstat -ano | findstr :{port}', shell=True)
            lines = result.decode().splitlines()

            print(1)

            pids = set()
            for line in lines:
                match = re.search(r'\s+(\d+)$', line.strip())
                if match:
                    pids.add(match.group(1))
                    
            for pid in pids:
                subprocess.run(f'taskkill /PID {pid} /F', shell=True)
                print(f"Killed PID {pid} on port {port}")
        except subprocess.CalledProcessError:
            print(f"No process is using port {port}")

if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = ServerWidget()
   sys.exit(app.exec_())