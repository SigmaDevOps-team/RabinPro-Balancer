# URLs
url = www.rabinpro.ir
push_url = url+'/api/push_order'


# database
database = 'rabinpro_balancer'
database_table_maps = {
    'orders': 'orders',
}
special_characters = ';!@#$%^&*<>|\\/'
database_server_config = {
    'user'               : 'admin',
    'password'           : 'Jd5UNFNm2xE8nhdTuZ39D675M5yR2eaw6FfF6bjZ9pbD8m5P8yZHkcUNpJUmVMY8',
    'host'               : 'localhost',
    'connect_timeout'    : 15,
}

#
max_push_retry = 3
max_cancel_retry = 5
wait_after_push = 30

#
pushed_status = 1
canceled_status = 2