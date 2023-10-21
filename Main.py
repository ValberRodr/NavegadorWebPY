import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QToolBar, QAction, QLineEdit, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class WebBrowser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))

        self.browser.urlChanged.connect(self.update_urlbar)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(self.layout)

        self.setCentralWidget(container)

        navtb = QToolBar("Navigation")
        self.addToolBar(navtb)

        back_btn = QAction("Back", self)
        back_btn.setStatusTip("Back to previous page")
        back_btn.triggered.connect(self.browser.back)
        navtb.addAction(back_btn)

        next_btn = QAction("Forward", self)
        next_btn.setStatusTip("Forward to next page")
        next_btn.triggered.connect(self.browser.forward)
        navtb.addAction(next_btn)

        reload_btn = QAction("Reload", self)
        reload_btn.setStatusTip("Reload page")
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)

        home_btn = QAction("Home", self)
        home_btn.setStatusTip("Go home")
        home_btn.triggered.connect(self.navigate_home)
        navtb.addAction(home_btn)

        navtb.addSeparator()

        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        stop_btn = QAction("Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        stop_btn.triggered.connect(self.browser.stop)
        navtb.addAction(stop_btn)

        navtb.addSeparator()

        history_btn = QAction("History", self)
        history_btn.setStatusTip("Show history")
        history_btn.triggered.connect(self.show_history)
        navtb.addAction(history_btn)

        self.statusBar()

        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")

        open_file_action = QAction("Open File", self)
        open_file_action.setStatusTip("Open from file")
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)

        save_file_action = QAction("Save Page", self)
        save_file_action.setStatusTip("Save current page to file")
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)

        print_action = QAction("Print", self)
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.print_page)
        file_menu.addAction(print_action)

        edit_menu = menubar.addMenu("Edit")

        find_action = QAction("Find", self)
        find_action.setStatusTip("Find on page")
        find_action.triggered.connect(self.find_text)
        edit_menu.addAction(find_action)

        view_menu = menubar.addMenu("View")

        fullscreen_action = QAction("Toggle Fullscreen", self)
        fullscreen_action.setShortcut("F11")
        fullscreen_action.setStatusTip("Toggle fullscreen mode")
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        view_menu.addAction(fullscreen_action)

        # Add a URL bar

    def update_urlbar(self, q):
        if q.scheme() == '':
            # The user has simply typed a query, not a URL
            q.setUrl(QUrl("http://" + q.toString()))

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == '':
            q.setUrl("http://" + self.urlbar.text())

        self.browser.setUrl(q)

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://z74cl.sharepoint.com/sites/GovMatriz"))

    def show_history(self):
        history = self.browser.history()
        for history_entry in history:
            print("Visited: ", history_entry.url().toString())

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Page", "", "Hypertext Markup Language (*.htm *.html);;"
                                                                   "All files (*)")

        if file_name:
            with open(file_name, 'r') as f:
                html = f.read()
            self.browser.setHtml(html)
            self.urlbar.setText(file_name)

    def save_file(self):
        file_name, _ = QFileDialog.getSaveAsFileName(self, "Save Page As", "", "Hypertext Markup Language (*.htm *html);;"
                                                                       "All files (*)")

        if file_name:
            with open(file_name, 'w') as f:
                f.write(self.browser.page().toHtml())
                self.urlbar.setText(file_name)

    def print_page(self):
        dlg = QPrintDialog()
        if dlg.exec_():
            self.browser.print(dlg.printer())

    def find_text(self):
        self.browser.findText("")

    def toggle_fullscreen(self, checked):
        if checked:
            self.showFullScreen()
        else:
            self.showNormal()

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Simple Web Browser")
    window = WebBrowser()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
