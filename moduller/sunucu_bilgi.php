$dizi = array(
    "uname" => php_uname(),
    "user" => get_current_user(),
    "version" => phpversion(),
    "safe_mode" => ini_get('safe_mode'),
    "ip" => $_SERVER['SERVER_ADDR'],
    "date" => date("d.m.Y H:i:s"),
    "pwd" => getcwd(),
    "software" => $_SERVER['SERVER_SOFTWARE']
);
echo json_encode($dizi);