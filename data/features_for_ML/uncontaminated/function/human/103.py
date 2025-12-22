def apply_format():
            self.log_config["date_style"] = date_style_var.get()
            self.log_config["log_level_style"] = level_style_var.get()
            self.log_config["color_text"] = color_text_var.get()

            # 重新初始化格式化器
            self.formatter = LogFormatter(self.log_config, self.custom_module_colors, self.custom_level_colors)
            self.log_display.formatter = self.formatter
            self.log_display.configure_text_tags()

            # 保存配置
            self.save_viewer_config()

            # 重新过滤日志以应用新格式
            self.filter_logs()

            format_window.destroy()