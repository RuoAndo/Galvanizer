 python viz.py libxl_list_cpupool > tmpdot
 dot -o c.png -Tpng tmpdot
 cp c.png /var/www/html/codes/1c.png