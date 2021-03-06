<?php
if (!isset($_SERVER['HTTP_X_FORWARDED_FOR'])) {
  $client_ip = $_SERVER['REMOTE_ADDR'];
} else {
  $client_ip = $_SERVER['HTTP_X_FORWARDED_FOR'];
}
if(isset($_GET['service'])) {
  $verzeichnis = "/var/python";
  $docs = 'docs';
} else {
  $verzeichnis = "/var/www";
  $docs = 'httpd';
}
if (is_dir($verzeichnis)) {
  if ($handle = opendir($verzeichnis)) {
    while (($file = readdir($handle)) !== false) {
      if ($file != '.' && $file != '..' && $file != 'phpmyadmin' && $file != 'html') {
      $subdomain_data = str_getcsv(explode(';', str_replace("\n", ";", file_get_contents($verzeichnis.'/'.$file.'/.data.csv')))[1], ',');
      if($subdomain_data[1]) {
        if(is_dir($verzeichnis.'/'.$subdomain_data[1].'/'.$docs.'/.git')) {
            $key = hash('sha512', file_get_contents($verzeichnis.'/'.$subdomain_data[1].'/.data.csv'));
            if(isset($_GET[$key])) {
              echo '<code>cd '.$verzeichnis.'/'.$subdomain_data[1].'/'.$docs.' ; git fetch --all ; git reset --hard origin/master ; git pull origin master ; git reset --hard main ; git pull origin main</code><br>';
              echo shell_exec('cd '.$verzeichnis.'/'.$subdomain_data[1].'/'.$docs.' ; git fetch --all ; git reset --hard origin/master ; git pull origin master ; git reset --hard main ; git pull origin main');
              echo shell_exec('chmod -R 777 '.$verzeichnis.'/'.$subdomain_data[1].'/'.$docs);
              if($subdomain_data[1] == 'webservermanagementsystem') { // Damit das Webservermanagement System auch richtig geupdatet wird.
                echo shell_exec('sudo service webservermanagementsystem stop');
                echo shell_exec('sudo service webservermanagementsystem start');
              }
            } else {
              $key_error = true;
            }
          if(isset($key_error)) {
              $file_key_error = file_get_contents('key_error.inc.txt');
              file_put_contents('key_error.inc.txt', $file_key_error."Key Error:  ".$client_ip." ".date('s.i.H.d.m.Y').";\n");
            }
          }
          unset($file_key_error);
          unset($main_domain);
          unset($key_error);
        }
      }
      }
    }
  }
?>
