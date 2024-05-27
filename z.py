import lynxy

lynxy.enable_print()
ip = input('-> ')
lynxy.start_client(ip)
lynxy.submit_username_data('SketchedDoughnut')
# lynxy.request_username_data('SketchedDoughnut')
lynxy.submit_username_data('SketchedDoughnut2')
lynxy.request_username_data('SketchedDoughnut3') # incorrect username
lynxy.request_username_data('SketchedDoughnut')
lynxy.send_msg('end_session')
lynxy.shutdown_client()