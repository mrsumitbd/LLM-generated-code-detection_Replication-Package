import os
import time
from prompt_toolkit import Application
from prompt_toolkit.layout.containers import HSplit, Window, ConditionalContainer
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.filters import Condition
from prompt_toolkit.widgets import TextArea
from prompt_toolkit.history import FileHistory

class NanoEditor:
    def __init__(self, filename):
        self.filename = filename
        self.dirty = False
        self.statusmsg = ""
        self.statusmsg_time = 0
        self.syntax = None
        self.search_mode = False
        self.search_query = ""
        self.search_history = []
        self.search_results = []
        self.current_search_index = -1
        self.last_search_query = ""

        # 初始化语法高亮数据库
        c_extensions = [".c", ".h", ".cpp", ".hpp", ".cc"]
        c_keywords = [
            "auto", "break", "case", "continue", "default", "do", "else", "enum",
            "extern", "for", "goto", "if", "register", "return", "sizeof", "static",
            "struct", "switch", "typedef", "union", "volatile", "while", "NULL",
            "alignas", "alignof", "and", "and_eq", "asm", "bitand", "bitor", "class",
            "compl", "constexpr", "const_cast", "deltype", "delete", "dynamic_cast",
            "explicit", "export", "false", "friend", "inline", "mutable", "namespace",
            "new", "noexcept", "not", "not_eq", "nullptr", "operator", "or", "or_eq",
            "private", "protected", "public", "reinterpret_cast", "static_assert",
            "static_cast", "template", "this", "thread_local", "throw", "true", "try",
            "typeid", "typename", "virtual", "xor", "xor_eq",
            "int|", "long|", "double|", "float|", "char|", "unsigned|", "signed|",
            "void|", "short|", "auto|", "const|", "bool|"
        ]

        self.HLDB = [
            EditorSyntax(
                c_extensions,
                c_keywords,
                "//",
                "/*",
                "*/",
                HL_HIGHLIGHT_STRINGS | HL_HIGHLIGHT_NUMBERS
            )
        ]

        # 选择语法高亮
        self.select_syntax_highlight()

        # 创建文本区域
        self.text_area = TextArea(
            text=self.load_file(),
            lexer=NanoLexer(self.syntax) if self.syntax else None,
            scrollbar=True,
            line_numbers=True,
            multiline=True,
            wrap_lines=False,
            history=FileHistory('.nano_history'),
            auto_suggest=AutoSuggestFromHistory(),
            style='class:editor'
        )

        # 搜索输入框
        self.search_input = TextArea(
            height=1,
            prompt="搜索: ",
            style='class:search',
            multiline=False,
            wrap_lines=False,
            history=FileHistory('.nano_search_history'),
            auto_suggest=AutoSuggestFromHistory(),
        )

        # 状态栏
        self.status_bar = Window(
            content=FormattedTextControl(self.get_status_text),
            height=1,
            style="class:status"
        )

        # 消息栏
        self.message_bar = Window(
            content=FormattedTextControl(self.get_message_text),
            height=1,
            style="class:message"
        )

        # 创建布局
        self.root_container = HSplit([
            self.text_area,
            self.status_bar,
            ConditionalContainer(
                content=self.search_input,
                filter=Condition(lambda: self.search_mode)
            ),
            self.message_bar
        ])

        # 创建按键绑定
        self.bindings = KeyBindings()
        self.setup_key_bindings()

        # 创建样式
        self.style = Style([
            ('status', 'bg:#0055ff fg:#ffffff'),
            ('message', 'bg:#00aa00 fg:#ffffff'),
            ('search', 'bg:#222222 fg:#ffffff'),
            ('keyword1', 'fg:#ff5555 bold'),
            ('keyword2', 'fg:#5555ff bold'),
            ('string', 'fg:#00aa00'),
            ('number', 'fg:#aa00aa'),
            ('comment', 'fg:#888888 italic'),
            ('search_match', 'bg:#555500 fg:#ffffff'),
        ])

        # 创建应用
        self.application = Application(
            layout=Layout(self.root_container, focused_element=self.text_area),
            key_bindings=self.bindings,
            mouse_support=True,
            style=self.style,
            full_screen=True
        )

    def select_syntax_highlight(self):
        """根据文件名选择语法高亮方案"""
        if not self.filename:
            return

        for syntax in self.HLDB:
            for pattern in syntax.filematch:
                if pattern.startswith('.'):
                    # 文件扩展名匹配
                    if self.filename.endswith(pattern):
                        self.syntax = syntax
                        return
                else:
                    # 文件名包含匹配
                    if pattern in self.filename:
                        self.syntax = syntax
                        return

    def load_file(self):
        """加载文件内容"""
        try:
            with open(self.filename, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return ""
        except Exception as e:
            return f"Error opening file: {e}"

    def save_file(self):
        """保存文件"""
        try:
            with open(self.filename, 'w') as f:
                f.write(self.text_area.text)
            self.dirty = False
            self.set_status_message(f"文件保存成功, {len(self.text_area.text)} 字节写入磁盘.")
            return True
        except Exception as e:
            self.set_status_message(f"文件保存失败! I/O 错误: {str(e)}.")
            return False

    def set_status_message(self, message, *args):
        """设置状态消息"""
        self.statusmsg = message % args if args else message
        self.statusmsg_time = time.time()

    def get_status_text(self):
        """获取状态栏文本"""
        status = f"{os.path.basename(self.filename)} - {len(self.text_area.text.splitlines())} 行"
        if self.dirty:
            status += " (已修改)"
        return status

    def get_message_text(self):
        """获取消息栏文本"""
        if self.statusmsg and time.time() - self.statusmsg_time < 5:
            return self.statusmsg

        if self.search_mode:
            if self.search_results:
                return f"找到 {len(self.search_results)} 个匹配项 - 按 F3 查找下一个, Shift+F3 查找上一个, ESC 退出"
            return f"搜索模式 - 输入搜索词后按 Enter 开始搜索, ESC 退出"

        return "帮助: Ctrl-S = 保存文件 | Ctrl-Q = 退出编辑 | Ctrl-F = 查找 | F3 = 查找下一个"

    def start_search(self):
        """启动搜索模式"""
        self.search_mode = True
        self.search_results = []
        self.current_search_index = -1

        # 使用上一次的搜索词
        if self.last_search_query:
            self.search_input.text = self.last_search_query

        # 设置焦点到搜索输入框
        self.application.layout.focus(self.search_input)
        self.set_status_message("输入搜索词后按 Enter 开始搜索")

    def end_search(self):
        """结束搜索模式"""
        self.search_mode = False
        # 保存搜索词历史
        if self.search_query and self.search_query not in self.search_history:
            self.search_history.append(self.search_query)
        # 更新词法分析器，移除搜索高亮
        self.text_area.lexer = NanoLexer(self.syntax)
        # 设置焦点回主文本区域
        self.application.layout.focus(self.text_area)
        self.set_status_message("结束搜索模式")

    def perform_search(self, query=None):
        """执行搜索操作"""
        if query is None:
            query = self.search_input.text.strip()

        if not query:
            self.set_status_message("请输入搜索词")
            return False

        self.search_query = query
        self.last_search_query = query

        text = self.text_area.text
        self.search_results = []
        start = 0

        # 查找所有匹配项
        while True:
            pos = text.find(self.search_query, start)
            if pos == -1:
                break
            self.search_results.append(pos)
            start = pos + len(self.search_query)

        if self.search_results:
            self.current_search_index = -1
            self.set_status_message("找到 %d 个匹配项", len(self.search_results))

            # 更新词法分析器，添加搜索高亮
            self.text_area.lexer = NanoLexer(self.syntax, self.search_query)
            return True
        else:
            self.set_status_message("未找到匹配项: %s", self.search_query)
            return False

    def jump_to_search_result(self, index=None):
        """跳转到搜索结果"""
        if not self.search_results:
            return

        if index is None:
            index = self.current_search_index

        if index < 0 or index >= len(self.search_results):
            return

        self.current_search_index = index
        pos = self.search_results[self.current_search_index]

        # 设置光标位置
        self.text_area.buffer.cursor_position = pos

        # 滚动到可见区域
        self.text_area.buffer.cursor_position = pos
        self.text_area.buffer.cursor_position = pos + len(self.search_query)

        # 设置状态消息
        self.set_status_message("找到 %d 个匹配项, 当前第 %d 个",
                                len(self.search_results),
                                self.current_search_index + 1)

    def find_next(self):
        """查找下一个匹配项"""
        if not self.search_results:
            if not self.perform_search():
                return

        if self.current_search_index < 0:
            self.current_search_index = 0
        else:
            self.current_search_index = (self.current_search_index + 1) % len(self.search_results)

        self.jump_to_search_result()

    def find_previous(self):
        """查找上一个匹配项"""
        if not self.search_results:
            if not self.perform_search():
                return

        if self.current_search_index < 0:
            self.current_search_index = len(self.search_results) - 1
        else:
            self.current_search_index = (self.current_search_index - 1) % len(self.search_results)

        self.jump_to_search_result()

    def setup_key_bindings(self):
        """设置按键绑定"""
        kb = self.bindings

        @kb.add(CTRL_S)
        def _(event):
            self.save_file()

        @kb.add(CTRL_Q)
        def _(event):
            if self.dirty:
                self.set_status_message("警告!!! 文件存在未保存的修改。再按一次 Ctrl-Q 退出.")
                self.dirty = False
            else:
                event.app.exit()

        @kb.add(CTRL_F)
        def _(event):
            self.start_search()

        @kb.add('c-n')
        def _(event):
            self.find_next()

        @kb.add('c-p')
        def _(event):
            self.find_previous()

        @kb.add(ESC)
        def _(event):
            if self.search_mode:
                self.end_search()
            else:
                # 允许ESC退出应用
                event.app.exit()

        @kb.add('enter', filter=Condition(lambda: self.search_mode))
        def _(event):
            # 在搜索模式下按Enter，执行搜索
            if self.search_input.text.strip():
                self.perform_search()
                if self.search_results:
                    self.jump_to_search_result(0)
            else:
                self.set_status_message("请输入搜索词")

        # 文本变化时标记为已修改
        def on_text_changed(buf):
            self.dirty = True

        self.text_area.buffer.on_text_changed += on_text_changed

        # 搜索输入框变化时实时搜索
        def on_search_changed(buf):
            query = buf.text.strip()
            if query:  # 至少1个字符才实时搜索
                self.perform_search(query)
                if self.search_results:
                    self.jump_to_search_result(0)

        self.search_input.buffer.on_text_changed += on_search_changed

    def get_content(self):
        """获取当前编辑内容"""
        return self.text_area.text

    def run(self):
        """运行编辑器"""
        self.set_status_message("帮助: Ctrl-S = 保存文件 | Ctrl-Q = 退出编辑 | Ctrl-F = 查找 | F3 = 查找下一个")
        self.application.run()