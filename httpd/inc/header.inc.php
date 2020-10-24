<?php
  require('./inc/configdata.inc.php');
  include('./inc/dbaccessdata.inc.php');
  $data['full_domain'] = $_SERVER['REQUEST_SCHEME'].'://'.$_SERVER['HTTP_HOST'];
  $data['domainname'] = explode('.', $_SERVER['HTTP_HOST'])[1].'.'.explode('.', $_SERVER['HTTP_HOST'])[2].'.'.explode('.', $_SERVER['HTTP_HOST'])[3];

  // Eigene URL mit und ohne GET-Parameter
  if($_SERVER['SERVER_PORT']) {
	   $data['own_url_with_get'] = 'https://'.$_SERVER['HTTP_HOST'].$_SERVER['REQUEST_URI'];
	   $data['own_url'] = 'https://'.$_SERVER['HTTP_HOST'].explode('?', $_SERVER['REQUEST_URI'])[0];
  } else {
	   $data['own_url_with_get'] = 'http://'.$_SERVER['HTTP_HOST'].$_SERVER['REQUEST_URI'];
	   $data['own_url'] = 'http://'.$_SERVER['HTTP_HOST'].explode('?', $_SERVER['REQUEST_URI'])[0];
  }

  if(explode('.', $_SERVER['HTTP_HOST'])[0] != 'config') {
    die('Error 403. Bitte achte darauf, dass deine Subdomain mit <strong>config.</strong> beginnt.');
  }

  $authcode_hash = hash('sha512', '5si*YTGdtUdV1"gaF1>yOG^0C"rSRpca0WZ6:)nw1Xe,|$');
  // Wenn die App den richtigen `authcode` per GET übermittelt oder der COOKIE `authcode` gesetzt ist und mit dem oben generierten $authcode_hash übereinstimmt, wird das Configuration Panel angezeigt
  if($_COOKIE["authcode"] === $authcode_hash) {
    $show_site = true;
    // Ansonnsten wird das Anmeldeformular angezeigt
  } else {
	// Überprüft ob das Formular abgesendet wurde
    if(isset($_POST['authenticate'])) {
      // Überprüft ob das Passwortfeld Ihnalt hat und ob das Fake Captcha leer ist
      if(!empty($_POST['password'])) {
        // Überprüft das eingegebene Passwort mit dem Hash. Wenn dies übereinstimmt wird der Vertretungsplan angezeigt und der COOKIE `authcode` mit dem $authcode_hash für 12 Stunden gesetzt
        if (hash('sha512', 'd[0<~]PH'.$_POST['password'].'94j|i4BY') === $password_hash) {
          $show_site = true;
          setcookie("authcode", $authcode_hash, time() + (3600 * 12));
          // Wenn es nicht übereinstimmt wird die jeweilige Benachrichtigung angezeigt
        } else {
          $msg = 'Das<span style="color: transparent;">'.rand(0, 9).'</span>Passwort<span style="color: transparent;">'.rand(0, 9).'</span>war<span style="color: transparent;">'.rand(0, 9).'</span>leider<span style="color: transparent;">'.rand(0, 9).'</span>falsch'; // rand(0, 9), ist als Sicherheitsvorkehrung vor Brute Force Angriffen wie von hydra.
        }
        // Wenn das Passwort Feld leer ist oder das Captcha Feld ausgefüllt wurde, wird die jeweilige Benachrichtigung angezeigt
      } else {
        $msg = 'Bitte gebe ein Passwort ein';
      }
    }
  }

  // Code der nur ausgeführt werden darf, wenn der Nutzer eingeloggt ist
  if($show_site == true) {
    // Neue Subdomain anlegen
  	if(isset($_POST['newdomain'])) {
  		if(!empty($_POST['domainname']) && !empty($_POST['mail'])) {
  			if(!preg_match('/^[abcdefghijklmnopqrstuvwxyz0123456789\-.]+$/', $_POST['domainname'])) {
  				$error = true;
  				$msg = "Bitte halte dich beim Subdomain Namen an das richtige Format";
  			}
  			if (!filter_var($_POST['mail'], FILTER_VALIDATE_EMAIL)) {
  				$error = true;
  				$msg = "Bitte gebe eine gültige E-Mail-Adresse ein";
  			} else {
  				setcookie("mail", trim($_POST['mail']), time() + (3600*24*100));
  			}
  			if($_POST['domainname'][0] == '-' || $_POST['domainname'][2] == '-' || $_POST['domainname'][-1] == '-') {
  				$error = true;
  				$msg = 'Das erste, dritte und letzte Zeichen, darf kein Minuszeichen sein';
  			}
  			if(strlen($_POST['domainname']) > 62 || strlen($_POST['mail']) > 120) {
  				$error = true;
  				$msg = 'Bitte halte dich an die maximale Zeichenangabe';
  			}
  			$verzeichnis = "/var/www";
  			if (is_dir($verzeichnis)) {
  				if ($handle = opendir($verzeichnis)) {
  					while (($file = readdir($handle)) !== false) {
  						if(file_exists($verzeichnis.'/'.$file.'/.data.csv') && is_dir($verzeichnis.'/'.$file)) {
  							if($file == $_POST['domainname']) {
  								$error = true;
  								$msg = 'Dieser Domainname existiert bereits.';
  								break;
  							}
  						}
  					}
  				}
  			} else {
  				$msg = 'Etwas stimmt mit dem Webseitenordner nicht.';
  				$error = true;
  			}
  			if(!isset($error)) {
  				if($_POST['redirect'] == true) {
  					$redirect = '1';
  				} else {
  					$redirect = '0';
  				}
  				$domainname = trim($_POST['domainname']);
  				$mail = trim($_POST['mail']);
  				$result = shell_exec("sudo python3 /etc/apache2/new_domain.py ".$domainname." ".$mail." ".$redirect);
  				$msg = 'Domain wurde erfolgreich angelegt.';
  			}
  		} else {
  			$msg = "Bitte fülle alle Felder aus.";
  		}
  	}

    // Nutzer abmelden (alle Cookies löschen und zur Startseite weiterleiten)
    if (isset($_GET['logout'])) {
      setcookie ("authcode", "", time() - 3600);
      setcookie ("mail", "", time() - 3600);
      header("Location: ".$data['full_domain']);
    }

    // Subdomain löschen
  	if(isset($_GET['delete_domain'])) {
      if ($_SERVER['HTTP_HOST'] != $file) {
    		$result = shell_exec("sudo python3 /etc/apache2/remove_domain.py ".trim($_GET['delete_domain']));
    		if ($result == true) {
    			$msg = 'Die Domain wurde endgültig gelöscht.';
    		} else {
    			$msg = 'Es ist ein Fehler aufgetreten. Probiere es bitte erneut. Eventuell musst du die Domain manuell entfernen.';
    		}
      } else {
        $msg = 'Diese Seite kann nicht gelöscht werden, da es sich um die Seite handelt, auf der diese Meldung gerade angezeigt wird. Wenn diese Seite gelöscht werden würde, würde gar nichts mehr funktionieren.';
      }
      setcookie('msg', $msg, time() + 60);
	  header('Location: '.$data['own_url']);
  	}

    // https Weiterleitung entfernen
    if(isset($_GET['remove_https_redirect'])) {
      $result = shell_exec("sudo python3 /etc/apache2/remove_https_redirect.py ".trim($_GET['remove_https_redirect']));
      if ($result == true) {
  			$msg = 'Die https Weiterleitung wurde erfolgreich entfernt';
  		} else {
  			$msg = 'Es ist ein Fehler aufgetreten. Probiere es bitte erneut. Eventuell musst du die Weiterleitung manuell entfernen. Lösche dazu die .htaccess Datei und ändere in der .data.csv Datei beim Eintrag "redirection", die 1 zu einer 0.';
  		}
      setcookie('msg', $msg, time() + 60);
  		header('Location: '.$data['own_url']);
    }

    // https Weiterleitung hinzufügen
    if(isset($_GET['add_https_redirect'])) {
      $result = shell_exec("sudo python3 /etc/apache2/add_https_redirect.py ".trim($_GET['add_https_redirect']));
      if ($result == true) {
  			$msg = 'Die https Weiterleitung wurde erfolgreich hinzugefügt';
  		} else {
  			$msg = 'Es ist ein Fehler aufgetreten. Probiere es bitte erneut. Eventuell musst du die Weiterleitung manuell hinzufügen. Erstelle dazu eine .htaccess Datei (Im gleichen Verzeichnis, in der sich auch die .data.csv befindet) und ändere in der .data.csv Datei beim Eintrag "redirection", die 0 zu einer 1.';
  		}
      setcookie('msg', $msg, time() + 60);
  		header('Location: '.$data['own_url']);
    }

    // Manuelles Backup machen
    if(isset($_GET['make_manually_backup'])) {
      if (count(scandir('/var/www/'.$_GET['make_manually_backup'].'/httpd')) > 2) {
        $result = shell_exec("sudo python3 /etc/apache2/make_manually_backup.py ".trim($_GET['make_manually_backup']).' '.trim(str_replace('https://config.', '', $data['own_url']), '/'));
        if ($result == true) {
    			$msg = 'Es wurde erfolgreich ein manuelles Backup gemacht, welches sich <a href="'.$data['full_domain'].'/backups/'.trim($result).'" rel="download" alt="'.trim($result).'" title="Lade dir das eben gemachte Backup herunter."><strong>hier</strong></a> herunterladen lässt.';
    		} else {
    			$msg = 'Es ist ein Fehler aufgetreten. Probiere es bitte erneut. Eventuell musst du das Backup manuell machen.';
    		}
      } else {
        $msg = 'In diesem Verzeichnis sind noch keine Dateien vorhanden, sodass auch kein Backup gemacht werden kann.';
      }
        setcookie('msg', $msg, time() + 60);
    		header('Location: '.$data['own_url']);
    }

    // Manuelles gesamtes Backup machen
    if(isset($_GET['make_manually_whole_backup'])) {
      $counter = 0;
      $counter_fail = 0;
      $verzeichnis = "/var/www";
  		if (is_dir($verzeichnis)) {
  			if ($handle = opendir($verzeichnis)) {
  				while (($file = readdir($handle)) !== false) {
  					if(file_exists($verzeichnis.'/'.$file.'/.data.csv') && is_dir($verzeichnis.'/'.$file)) {
              if (count(scandir('/var/www/'.$file.'/httpd')) > 2) {
                $result = shell_exec("sudo python3 /etc/apache2/make_manually_backup.py ".trim($file).' '.trim(str_replace('https://config.', '', $data['own_url']), '/'));
                if ($result == false) {
                  $counter_fail++;
                }
                $counter++;
              }
            }
          }
        }
      }
      if ($counter_fail == 0) {
        if ($counter > 0) {
          if($counter == 1) {
            $msg = 'Es wurde von einer Seite ein Backup gemacht';
          } else {
            $msg = 'Es wurde von allen <strong>'.$counter.'</strong> Seiten ein Backup gemacht.';
          }
        } else {
          $msg = 'Es wurde keine Seite gefunden von der ein Backup hätte gemacht werden können.';
        }
      } else {
        if ($counter > 0) {
          if($counter == 1) {
            if($counter_fail == 1) {
              $msg = 'Es wurde von einer Seite ein Backup gemacht. Bei einer Seite trat ein Fehler auf. Bitte überprüfe manuell um welche Seite es sich dabei handelt.';
            } else {
              $msg = 'Es wurde von einer Seite ein Backup gemacht. Bei '.$counter_fail.' Seiten traten Fehler auf. Bitte überprüfe manuell um welche Seiten es sich dabei handelt.';
            }
          } else {
            $msg = 'Es wurde keine Seite gefunden von der ein Backup hätte gemacht werden können.';
          }
        } else {
          $msg = 'Es wurde keine Seite gefunden von der ein Backup hätte gemacht werden können.';
        }
      }
      setcookie('msg', $msg, time() + 60);
      header('Location: '.$data['own_url']);
    }

	// Gesamtes Backup der Datenbank machen
	if (isset($_GET['make_manually_whole_db_backup'])) {
    #Muss noch geschrieben werden
	}

    // SSL-Zertifikat erneuern
    if (isset($_GET['renew_ssl'])) {
      if (isset($_GET['email'])) {
        $result = shell_exec('sudo letsencrypt --apache -d '.$_GET['renew_ssl'].' --agree-tos -m '.$_GET['email'].' --no-eff-email --no-redirect --renew-by-default');
        if ($result == true) {
          $msg = '<abbr title="'.trim($result).'">Es scheint so, als ob alles funktioniert hat.</abbr>';
        } else {
          $msg = 'Es scheint so, als ob es nicht funktioniert hat.';
        }
      } else {
        $msg = 'Es wurde keine E-Mail überliefert, die bei der Erneuerung angegeben werden muss.';
      }
      setcookie('msg', $msg, time() + 60);
      header('Location: '.$data['own_url']);
    }

    // Config Passwort ändern
    if (isset($_POST['change_config_password'])) {
      include('./configdata.inc.php');
      // Config Passwort
      if(!empty($_POST['password'])) {
        $password_hash = hash("sha512", "d[0<~]PH".trim($_POST["password"])."94j|i4BY");
      }
      // SSH Passwort
      if (!empty($_POST['ssh_password'])) {
        $ssh_password = base64_encode($_POST['ssh_password']);
      }
      // SSH Nutzername
      if (!empty($_POST['ssh_username'])) {
        $ssh_username = trim($_POST['ssh_username']);
      }
      // Überprüfe ob die MySQL Zugangsdaten richtig sind
      if (!empty($_POST['mysql_password']) && !empty($_POST['mysql_username'])) {
        $check_mysql_password = $_POST['mysql_password'];
        $check_mysql_username = $_POST['mysql_username'];
      } elseif (!empty($_POST['mysql_password']) && empty($_POST['mysql_username'])) {
        $check_mysql_password = $_POST['mysql_password'];
        $check_mysql_username = $mysql_username;
      } elseif (empty($_POST['mysql_password']) && !empty($_POST['mysql_username'])) {
        $check_mysql_password = base64_decode($mysql_password);
        $check_mysql_username = $_POST['mysql_username'];
      } else {
        $check_mysql_password = base64_decode($mysql_password);
        $check_mysql_username = $mysql_username;
      }
      $db_link = mysqli_connect('localhost', $check_mysql_username, $check_mysql_password, 'phpmyadmin');
      if ($db_link == true) {
        // MySQL Passwort
        if (!empty($_POST['mysql_password'])) {
          $mysql_password = base64_encode($_POST['mysql_password']);
        }
        // MySQL Nutzername
        if (!empty($_POST['mysql_username'])) {
          $mysql_username = trim($_POST['mysql_username']);
        }
      } else {
        $msg = 'Es konnte sich nicht mit der MySQL-Datenbank verbunden werden. Die anderen einstellungen wurden gespeichert '.mysqli_error();
        $no_second_msg = true;
      }
      // Schreibe die Daten in die Konfigurationsdatei
      $data = '<?php
  $password_hash = "'.$password_hash.'";
  $ssh_password = "'.$ssh_password.'";
  $ssh_username = "'.$ssh_username.'";
  $mysql_password = "'.$mysql_password.'";
  $mysql_username = "'.$mysql_username.'";';
      file_put_contents('./inc/configdata.inc.php', $data);
      if(!isset($no_second_msg)) {
        $msg = 'Das Konfigurationseinstellungen wurde erfolgreich geändert.';
      }

      setcookie('msg', $msg, time() + 60);
      header('Location: '.explode('<', $data['own_url'])[0]);
    }
  }

  $service_verzeichnis = "/var/python";
  // Service von Github Klonen
  if (isset($_POST['service_repository_button'])) {
    if(isset($_POST['service_repository'])) {
      $headers = @get_headers($_POST['service_repository']);
      if($headers && strpos( $headers[0], '200')) {
        shell_exec('cd '.$service_verzeichnis.'/'.$_POST['service_repository_button'].' ; git clone '.trim($_POST['service_repository']));
        shell_exec('sudo rm -R '.$service_verzeichnis.'/'.$_POST['service_repository_button'].'/docs');
        shell_exec('sudo chmod -R 777 '.$service_verzeichnis.'/'.$_POST['service_repository_button']);
        $repository_name = array_reverse(explode("/", str_replace('.git', '', trim($_POST['service_repository']))))[0];
        rename($service_verzeichnis.'/'.$_POST['service_repository_button'].'/'.$repository_name, $service_verzeichnis.'/'.$_POST['service_repository_button'].'/docs');
        shell_exec('sudo chmod -R 777 '.$service_verzeichnis.'/'.$_POST['service_repository_button']);
        $msg = "Das Repository ".$repository_name." wurde geklont.";
      }
      else {
        $msg = "Leider wurde das Repository nicht gefunden";
      }
    }
  }

  $verzeichnis = "/var/www";
  // Von GitHub klonen
  if (isset($_POST['repository_button'])) {
    if(isset($_POST['repository']) && isset($_POST['domain_name'])) {
      $repository = trim($_POST['repository']);
      $domain_name = trim($_POST['domain_name']);
      $headers = @get_headers($repository);
      if($headers && strpos( $headers[0], '200')) {
        shell_exec('cd '.$verzeichnis.'/'.$domain_name.' ; git clone '.$repository);
        shell_exec('sudo rm -R httpd');
        shell_exec('sudo chmod -R 777 '.$verzeichnis.'/'.$domain_name);
        $domain_repository_name = array_reverse(explode("/", str_replace('.git', '', $repository)))[0];
        rename($verzeichnis.'/'.$domain_name.'/'.$domain_repository_name, $verzeichnis.'/'.$domain_name.'/httpd');
        shell_exec('sudo chmod -R 777 '.$verzeichnis.'/'.$domain_name);
        $msg = "Das Repository wurde geklont.";
      }
      else {
        $msg = "Leider wurde das Repository nicht gefunden";
      }
    }
  }

  // Neuen Service erstellen
  if(isset($_POST['newservice'])) {
    if(!empty($_POST['servicename'])) {
      if(!preg_match('/^[abcdefghijklmnopqrstuvwxyz0123456789]+$/', $_POST['servicename'])) {
        $error = true;
        $msg = "Bitte halte dich beim Service Namen an das richtige Format.";
      }
      if(strlen($_POST['servicename']) > 40) {
        $error = true;
        $msg = 'Bitte halte dich an die maximale Zeichenangabe';
      }
      if (is_dir($service_verzeichnis)) {
        if ($handle = opendir($service_verzeichnis)) {
          while (($file = readdir($handle)) !== false) {
            if(file_exists($service_verzeichnis.'/'.$file.'/.data.csv') && is_dir($service_verzeichnis.'/'.$file)) {
              if($file == $_POST['servicename'] || file_exists('/lib/systemd/system/'.$_POST['servicename'].'.service')) {
                $error = true;
                $msg = 'Dieser Service existiert bereits.';
                break;
              }
            }
          }
        }
      } else {
        $msg = 'Etwas stimmt mit dem Verzeichnisordner nicht.';
        $error = true;
      }
      if(!isset($error)) {
        if($_POST['autostart'] == true) {
          $autostart = '1';
        } else {
          $autostart = '0';
        }
        $servicename = trim($_POST['servicename']);
        $result = shell_exec("sudo python3 /etc/apache2/new_service.py ".$servicename." ".$autostart);
        $msg = 'Service wurde erfolgreich erstellt: '.$result;
      }
    } else {
      $msg = "Bitte fülle alle Felder aus.";
    }
  }

  // Service starten
  if(isset($_GET['start_service'])) {
    if(file_exists('/lib/systemd/system/'.$_GET['start_service'].'.service')) {
      shell_exec('sudo service '.$_GET['start_service'].' stop');
      sleep(1);
      $result = shell_exec('sudo service '.$_GET['start_service'].' start');
      $msg = 'Der Service wurde gestartet';
    } else {
      $mgs = 'Der Service wurde nicht gefunden...';
    }
  }

  // Service stoppen
  if(isset($_GET['stop_service'])) {
    if(file_exists('/lib/systemd/system/'.$_GET['stop_service'].'.service')) {
      $result = shell_exec('sudo service '.$_GET['stop_service'].' stop');
      $msg = 'Der Service wurde gestoppt';
    } else {
      $mgs = 'Der Service wurde nicht gefunden...';
    }
  }

  // Autostart aktivieren
  if(isset($_GET['append_autostart'])) {
    if(file_exists('/lib/systemd/system/'.trim($_GET['append_autostart']).'.service')) {
      $result = shell_exec('sudo python3 /etc/apache2/append_autostart.py '.trim($_GET['append_autostart']));
      $msg = 'Der Autostart wurde hinzugefügt: '.$result;
    } else {
      $mgs = 'Der Autostart ist wahrscheinlich bereits deaktiviert.';
    }
  }

  // Autostart entfernen
  if(isset($_GET['remove_autostart'])) {
    if(file_exists('/etc/init.d/'.trim($_GET['remove_autostart']).'.autostart')) {
      $result = shell_exec('sudo python3 /etc/apache2/remove_autostart.py '.trim($_GET['remove_autostart']));
      $msg = 'Der Autostart wurde entfernt: '.$result;
    } else {
      $msg = 'Der Autostart ist wahrscheinlich bereits deaktiviert.';
    }
  }

  // Service & Inhalt löschen
  if(isset($_GET['delete_content'])) {
      shell_exec('sudo python3 /etc/apache2/remove_service.py '.trim($_GET['delete_content']));
      $msg = 'Der Inhalt und Service wurde unwiderruflich gelöscht';
  }

  // Nachricht die in Cookie an die nächste Seite übermittelt wurde in $msg abspeichern
  if(!empty($_COOKIE['msg'])) {
    $msg = trim($_COOKIE['msg']);
    setcookie('msg', '', time() - 3600);
  }
  if(isset($msg)) {
    $msg_field = '<div class="message"><span onclick="this.parentElement.style.display=\'none\';" style="float: right; cursor: pointer;">×</span> '.trim($msg).'&nbsp;&nbsp;&nbsp;</div>';
  }
?>
<html lang="de">
	<head>
		<meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
		<title>Webserver Configuration Panel</title>
		<meta name="language" content="de">
		<meta name="date" content="2019-08-16">
		<meta name="keywords" content="webserver, configuration, panel">
		<meta name="description" content="Create domains with just one click and manage your server.">
		<meta name="robots" content="noindex, nofollow">
		<meta name="author" content="Tom Aschmann">
		<meta name="copyright" content="©2019-<?php echo date('Y'); ?> Tom Aschmann">
		<meta name="publisher" content="Tom Aschmann">
		<meta name="msapplication-TileColor" content="#38ada9">
		<meta name="theme-color" content="#38ada9">
		<meta name="msapplication-TileImage" content="./assets/icon/ms-icon-144x144.png">
		<meta http-equiv="language" content="deutsch, de">
		<link rel="apple-touch-icon" sizes="57x57" href="./assets/icon/apple-icon-57x57.png">
		<link rel="apple-touch-icon" sizes="60x60" href="./assets/icon/apple-icon-60x60.png">
		<link rel="apple-touch-icon" sizes="72x72" href="./assets/icon/apple-icon-72x72.png">
		<link rel="apple-touch-icon" sizes="76x76" href="./assets/icon/apple-icon-76x76.png">
		<link rel="apple-touch-icon" sizes="114x114" href="./assets/icon/apple-icon-114x114.png">
		<link rel="apple-touch-icon" sizes="120x120" href="./assets/icon/apple-icon-120x120.png">
		<link rel="apple-touch-icon" sizes="144x144" href="./assets/icon/apple-icon-144x144.png">
		<link rel="apple-touch-icon" sizes="152x152" href="./assets/icon/apple-icon-152x152.png">
		<link rel="apple-touch-icon" sizes="180x180" href="./assets/icon/apple-icon-180x180.png">
		<link rel="icon" type="image/png" sizes="192x192"	href="./assets/icon/android-icon-192x192.png">
		<link rel="icon" type="image/png" sizes="32x32" href="./assets/icon/favicon-32x32.png">
		<link rel="icon" type="image/png" sizes="96x96" href="./assets/icon/favicon-96x96.png">
		<link rel="icon" type="image/png" sizes="16x16" href="./assets/icon/favicon-16x16.png">
		<link rel="manifest" href="./assets/manifest.json">
		<link rel="stylesheet" type="text/css" href="./assets/style.css">
		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
	</head>
	<body>
		<?php
			if($show_site == true) {
		?>
		<header>
      <img src="./assets/icon/apple-icon-180x180.png">
      <nav>
          <a></a>
          <ul>
              <li><a href="">Startseite</a></li>
              <li><a href="http://<?php echo $_SERVER['REMOTE_ADDR']; ?>:8888?hostname=localhost&username=<?php echo $ssh_username; ?>&password=<?php echo $ssh_password; ?>&command=clear" target="popup" onclick="javascript:open('', 'popup', 'height=720,width=1280,resizable=yes')">SSH-Konsole</a></li>
              <!--<li><a href="">Dateimanager</a></li>-->
              <li><a href="<?php echo $_SERVER['REQUEST_SCHEME'].'://'.'phpmyadmin.'.$data['domainname'] ?>" target="_blank">PhpMyAdmin</a></li>
              <li><a href="?logout">Abmelden</a></li>
          </ul>
      </nav>
		</header>
		<?php
			}
		?>
		<article>
		<?php
			if($show_site == false) {
		?>
			<section>
				<form method="post">
					<h3>Webserver Configuration Panel</h3>
					<h4>Logge dich ein, um den Webserver zu verwalten</h4>
					<?php if(!empty($msg)) { ?>
						<h4><?php echo $msg; ?></h4>
					<?php } ?>
					<label>Passwort:
						<input type="password" name="password" placeholder="Passwort" title="Gebe hier das Passwort ein um auf das Webserver Configuration Panel zuzugreifen" maxlength="64" autofocus required>
					</label>
					<button type="submit" name="authenticate" title="Du bleibt für 12 Stunden angemeldet">Anmelden</button>
				</form>
			</section>
		<?php
			}
		?>
