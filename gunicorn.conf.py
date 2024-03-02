wsgi_app = "main:app"
bind = "0.0.0.0:7999"
daemon = False
workers = 4
threads = 2
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 1200
reload = False


# import traceback
# import io

# timeout 時に呼び出される関数?
# 呼び出されない
# def worker_abort(worker):
#     debug_info = io.StringIO()
#     debug_info.write("Traceback at time of timeout:\n")
#     traceback.print_stack(file=debug_info)
#     worker.log.critical(debug_info.getvalue())
