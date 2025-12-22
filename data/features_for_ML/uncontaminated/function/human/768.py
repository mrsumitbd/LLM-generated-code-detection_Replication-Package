def run_analysis():
            try:
                global currentAnalysis
                report = analyze_stock_streaming(stock_code, enable_streaming, client_id)
                currentAnalysis = report
                logger.info(f"股票流式分析完成: {stock_code}")
            except Exception as e:
                logger.error(f"股票流式分析失败: {stock_code}, 错误: {e}")
            finally:
                with task_lock:
                    analysis_tasks.pop(stock_code, None)