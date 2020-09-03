<ul style="padding:15px;">
<?php
  $dateien = scandir('/var/www/config.'.$data['domainname'].'/httpd/'.$_GET['dir']);
  foreach ($dateien as $datei) {
    if ($datei != '..' && ($datei != '.' || isset($_GET['dir']))) {
      if ($datei == '.' && $_GET['dir'] != '.') {
        echo '<li><a href="'.explode('&', $data['own_url_with_get'])[0].'&dir='.$datei.'" rel="directory" alt="open folder" title="Öffne diesen Ordner">'.$datei.'</a></li>';
        echo $_GET['dir'];
      } elseif (is_dir($datei)) {
        $dir = true;
        echo '<a href="'.explode('&', $data['own_url_with_get'])[0].'&dir='.$datei.'" rel="directory" alt="open folder" title="Öffne diesen Ordner">'.$datei.'</a><br></li>';
      } else {
        $dir = false;
        echo '<li>'.$datei.'</li>';
      }
    }
  }
?>
</ul>
