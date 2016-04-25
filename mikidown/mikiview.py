import re
import platform

from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets, QtWebKitWidgets
"""
from PyQt4.QtCore import QDir, QPoint, QTimer, QUrl
from PyQt4.QtGui import QDesktopServices
from PyQt4.QtWebKit import QWebView, QWebPage
"""
import markdown

class MikiView(QtWebKitWidgets.QWebView):

    def __init__(self, parent=None):
        super(MikiView, self).__init__(parent)
        self.parent = parent

        self.fileUrlPrefix = "file://"
        if platform.system() == "Windows":
            self.fileUrlPrefix = "file:///"

        self.settings().clearMemoryCaches()
        self.notePath = parent.settings.notePath
        self.notebookPath = parent.settings.notebookPath
        cssurl = QtCore.QUrl(self.fileUrlPrefix+self.parent.settings.cssfile)
        self.settings().setUserStyleSheetUrl(cssurl)
        print(cssurl)
        self.page().setLinkDelegationPolicy(QtWebKitWidgets.QWebPage.DelegateAllLinks)

        self.page().linkClicked.connect(self.linkClicked)
        self.page().linkHovered.connect(self.linkHovered)
        self.page().mainFrame(
        ).contentsSizeChanged.connect(self.contentsSizeChanged)

        self.scrollPosition = QtCore.QPoint(0, 0)

    def linkClicked(self, qurl):
        '''three kinds of link:
            external uri: http/https
            page ref link:
            toc anchor link: #
        '''
        name = qurl.toString()
        print("linkClicked - name: ", name)
        http = re.compile('https?://')
        if http.match(name):                        # external uri
            QtGui.QDesktopServices.openUrl(qurl)
            return

        self.load(qurl)
        name = name.replace(self.fileUrlPrefix, '')
        name = name.replace(self.notePath, '').split('#')
        item = self.parent.notesTree.pageToItem(name[0])
        if not item or item == self.parent.notesTree.currentItem():
            return
        else:
            self.parent.notesTree.setCurrentItem(item)
            if len(name) > 1:
                link = self.fileUrlPrefix + self.notePath + "/#" + name[1]
                self.load(QtCore.QUrl(link))
            viewFrame = self.page().mainFrame()
            self.scrollPosition = viewFrame.scrollPosition()

    def linkHovered(self, link, title, textContent):
        '''show link in status bar
            ref link shown as: /parent/child/pageName
            toc link shown as: /parent/child/pageName#anchor (ToFix)
        '''
        # TODO: link to page by: /parent/child/pageName#anchor
        print("linkHovered - link: ", link)
        if link == '':                              # not hovered
            self.parent.statusBar.showMessage(self.parent.notesTree.currentPage())
        else:                                       # beautify link
            link = link.replace(self.fileUrlPrefix, '')
            link = link.replace(self.notePath, '')
            self.parent.statusBar.showMessage(link)

    def contentsSizeChanged(self, newSize):
        '''scroll notesView while editing (adding new lines)
           Whithout this, every `updateView` will result in scroll to top.
        '''
        if self.scrollPosition == QtCore.QPoint(0, 0):
            return
        viewFrame = self.page().mainFrame()
        newY = self.scrollPosition.y(
        ) + newSize.height() - self.contentsSize.height()
        self.scrollPosition.setY(newY)
        viewFrame.setScrollPosition(self.scrollPosition)

    def updateView(self):
        # url_notebook = self.fileUrlPrefix + os.path.join(self.notePath, '/')
        viewFrame = self.page().mainFrame()
        # Store scrollPosition before update notesView
        self.scrollPosition = viewFrame.scrollPosition()
        self.contentsSize = viewFrame.contentsSize()
        url_notebook = self.fileUrlPrefix + self.notePath 
        html = self.parent.notesEdit.toHtml()
        self.setHtml(html, QtCore.QUrl(url_notebook))
        # Restore previous scrollPosition
        viewFrame.setScrollPosition(self.scrollPosition)

    def updateLiveView(self):
        if self.parent.actions.get('split').isChecked():
            QtCore.QTimer.singleShot(1000, self.updateView)

