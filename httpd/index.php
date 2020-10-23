<?php
	require('./inc/header.inc.php');
	if($show_site == true) {
		$verzeichnis = "/var/www";
?>
	<section id="domains">
		<?php
		if (is_dir($verzeichnis)) {
			if ($handle = opendir($verzeichnis)) {
				while (($file = readdir($handle)) !== false) {
					if(file_exists($verzeichnis.'/'.$file.'/.data.csv') && is_dir($verzeichnis.'/'.$file.'/httpd')) {
						$subdomain_data = str_getcsv(explode(';', str_replace("\n", ";", file_get_contents($verzeichnis.'/'.$file.'/.data.csv')))[1], ',');
						if ($subdomain_data[3] == '1') {
							$request_scheme = 'https://';
						} else {
							$request_scheme = 'http://';
						}
						?>
							<section id="domain_index_<?php echo $subdomain_data[1]; ?>">
								<div class="header">
									<h1><a href="<?php echo $request_scheme.$file; ?>" rel="external" alt="<?php $subdomain_data[1]; ?>" title="Rufe die Subdomain <?php echo $file; ?> in einem neuen Tab auf" target="_blank"><?php echo $file; ?></a></h1>
								</div>
								<div class="second_header">
									<span class="header_item sitepath">Webseite unter <a href="?directory_content=<?php echo trim($file); ?>" rel="edit" alt="show directory content" title="Rufe den Verzeichnisinhalt auf um Dateien Verwalten zu können die in dem Ordner der Subdomain liegen."><?php echo $verzeichnis.'/'.$file.'/'; ?></a></span><br>
									<span class="header_item page_created">Webseite erstellt am: <strong><?php echo $subdomain_data[0]; ?> Uhr</strong></span><br>
									<span class="header_item https_redirect"><strong>Https Weiterleitung: </strong><?php if ($subdomain_data[3] == '1') { echo 'Ja - <a href="?remove_https_redirect='.trim($file).'" rel="remove" alt="remove https redirect" title="Die Weiterleitung, die in der .htaccess Datei vorhanden ist, wird entfernt. Dadurch wird die gesamte .htaccess Datei gelöscht.">Weiterleitung entfernen</a>'; } else { echo 'Nein - <a href="?add_https_redirect='.trim($file).'" rel="add" alt="add https redirect" title="Es wird eine .htaccess Datei erstellt, die eine https Weiterleitung erzwingt.">Weiterleitung hinzufügen</a>'; } ?></span><br>
									<span class="header_item ssl_email"><strong>SSL E-Mail-Adresse: </strong><a href="mailto:<?php echo $subdomain_data[2]; ?>?subject=Information%20wegen%20der%20Webseite:%20<?php echo trim($file); ?>&body=Hallo,%20%0D%0A%0D%0A" rel="mail" alt="send e-mail to subdomainowner" title="Sende dem Inhaber der Subdomain eine E-Mail, um ihn gegebenenfalls zu informieren, falls sich etwas an seiner Subdomain ändert."><?php echo $subdomain_data[2]; ?></a></span><br>
									<span class="header_item github"><strong>GitHub: </strong>
										<?php
											if (count(scandir($verzeichnis.'/'.$subdomain_data[1].'/httpd')) > 2) {
												if (!is_dir($verzeichnis.'/'.$subdomain_data[1].'/httpd/.git')) {
													echo 'Das Verzeichnis ist nicht leer.';
												} else {
													$key = hash('sha512', file_get_contents($verzeichnis.'/'.$subdomain_data[1].'/.data.csv'));
													$github_repo_link = explode("\n", explode('url = ', file_get_contents($verzeichnis.'/'.$subdomain_data[1].'/httpd/.git/config'))[1])[0];
													if (array_reverse(explode('.', $github_repo_link))[0] != 'git') {
														$github_repo_webhook_link = $github_repo_link.'/settings/hooks/new';
													} else {
														$github_repo_webhook_link = str_replace('.git', '/settings/hooks/new', $github_repo_link);
													}
													$copy_value_rand = rand(999999, 9999999);
													?>
													<script>
														function copy<?php echo $copy_value_rand; ?>() {
															  const el = document.createElement('textarea');
															  el.value = "<?php echo $data['own_url'].'webhook.php?'.$key; ?>";
															  document.body.appendChild(el);
															  el.select();
															  document.execCommand('copy');
															  document.body.removeChild(el);
														}
													</script>
													<strong>Webhook Link</strong>
													<a onclick="copy<?php echo $copy_value_rand; ?>()" href="<?php echo $github_repo_webhook_link; ?>" target="_blank" style="cursor: pointer; display: inline-table; width: 280px;">
														<input type="text" value="<?php echo $data['own_url'].'webhook.php?'.$key; ?>" size="" title="Gebe diesen Link unter <?php echo $github_repo_webhook_link; ?> ein. Empfolen sind die vorgegebenen Einstellungen. Mit klick hierdrauf, wird der Link automatisch kopiert." style="cursor: pointer;" readonly>
														<small><i>Webhok Link kopieren und Einstellungen öffnen</i></small>
													</a>
													<?php
												}
											} else {
										?>
										<form method="post">
											<label for="inputRepository">
												<input type="text" name="repository" id="inputRepository" title="Trage hier ein Repository von der Plattform GitHub ein, um es zu klonen." alt="github repository" placeholder="https://github.com/nutzername/repository-name" maxlength="255" autocomplete="off" required>
											</label>
											<input type="hidden" name="domain_name" value="<?php echo $subdomain_data[1]; ?>">
											<button type="submit" name="repository_button" title="Stelle eine Verbindung zum Repository her.">Klonen</button>
										</form>
										<?php
											}
										?>
										<p><?php if(isset($status)) { echo $status; } ?></p>
									</span><br>
								</div>
								<div class="third_header">
									<span class="header_item make_manually_backup"><?php if (count(scandir('/var/www/'.$file.'/httpd')) > 2) { ?><a href="?make_manually_backup=<?php echo trim($file); ?>" rel="backup" alt="make manually backup" title="Mache ein manuelles Backup aller Verzeichnisinhalte des ./htdocs/ Ordners.">Backup machen</a><?php } else { ?><abbr title="In diesem Verzeichnis sind noch keine Dateien vorhanden, sodass auch kein Backup gemacht werden kann." class="prohibited_link">Backup machen</abbr><?php } ?></span>
									<span class="header_item delete_domain"><?php if ($_SERVER['HTTP_HOST'] != $file) { ?><a href="?delete_domain=<?php echo trim($file); ?>" rel="delete" alt="delete site" title="Die Seite wird mit allen Daten endgültig gelöscht. 𝘼𝙘𝙝𝙩𝙪𝙣𝙜, 𝙙𝙞𝙚𝙨𝙚𝙧 𝙑𝙤𝙧𝙜𝙖𝙣𝙜 𝙠𝙖𝙣𝙣 𝙣𝙞𝙘𝙝𝙩 𝙧ü𝙘𝙠𝙜ä𝙣𝙜𝙞𝙜 𝙜𝙚𝙢𝙖𝙘𝙝𝙩 𝙬𝙚𝙧𝙙𝙚𝙣. Mache sicherheitshalber vorher ein Backup der Seite.">Seite löschen</a><?php } else { ?><abbr title="Diese Seite kann nicht gelöscht werden, da es sich um die Seite handelt, auf der diese Meldung gerade angezeigt wird. Wenn diese Seite gelöscht werden würde, würde gar nichts mehr funktionieren." class="prohibited_link">Seite löschen</abbr><?php } ?></span>
									<span class="header_item renew_ssl"><a href="?renew_ssl=<?php echo trim($file); ?>&email=<?php echo $subdomain_data[2]; ?>" rel="renew" alt="renew ssl certificate" title="Erneuere das SSL Zertifikat, falls du beim Aufrufen der Seite eine Meldung wie z. B.: Warnung: Mögliches Sicherheitsrisiko erkannt; bekommst. Wenn die Erneuerung nicht funktioniert, klicke nicht mehrmals oder generell unnötigerweise auf 'SSL-Zertifikat erneuern', da es passieren kann, dass die Subdomain, IP-Adresse oder deine E-Mail-Adresse für ein paar Tage gesperrt werden. Probiere es dann am besten eine Woche später erneut. Sollte auch dies nicht funktionieren, warte wieder ein paar Tage, mache ein Backup von all deinen Daten, lösche die Subdomain und benutze eine andere E-Mail-Adresse zum neu erstellen des Subdomains. Normalerweise muss es keine manuelle Erneuerung geben, da das SSL-Zertifikat automatisch erneuert wird. Wenn der Server allerdings nicht 24/7 angeschaltet ist, kann es passieren, dass das Zertifikat vor der nächsten automatischen Erneuerung abläuft. In so einem Fall kann man auf diese Funktion zurückgreifen.">SSL-Zertifikat erneuern</a></span>
								</div>
							</section>
						<?php
					}
				}
				closedir($handle);
			}
		}
		?>

<!-- Hier werden die einzelnen Service eingestellt -->
<?php
$service_verzeichnis = "/var/python";
if (is_dir($service_verzeichnis)) {
	if ($handle_service = opendir($service_verzeichnis)) {
		while (($file = readdir($handle_service)) !== false) {
			if(file_exists($service_verzeichnis.'/'.$file.'/.data.csv') && is_dir($service_verzeichnis.'/'.$file.'/docs')) {
				$service_data = str_getcsv(explode(';', str_replace("\n", ";", file_get_contents($service_verzeichnis.'/'.$file.'/.data.csv')))[1], ',');

				// Überprüfe den Status des Service
				$check_status_result = shell_exec('sudo service '.$file.' status | grep Active');
				$service_status = trim(explode(' since ', $check_status_result)[0]);
				$service_status_check = explode(' ', trim($service_status))[1];
				$service_status_time = trim(explode(' since ', $check_status_result)[1]);
				?>
					<section id="service_index_<?php echo $service_data[1]; ?>">
						<div class="header">
							<h1><?php echo $file; ?></h1>
						</div>
						<div class="second_header">
							<span class="header_item sitepath">Service unter <a href="?directory_content=<?php echo trim($file); ?>&service=1" rel="edit" alt="show directory content" title="Rufe den Verzeichnisinhalt auf, um Dateien Verwalten zu können die in dem Ordner liegen."><?php echo $service_verzeichnis.'/'.$file.'/docs'; ?></a></span><br>
							<span class="header_item content_created">Service erstellt am: <strong><?php echo $service_data[0]; ?> Uhr</strong></span><br>
							<?php if ('webservermanagementsystem' != $file) { ?><span class="header_item autostart"><strong>Autostart: </strong><?php if ($service_data[2] == '1') { echo 'Ja - <a href="?remove_autostart='.trim($file).'" rel="remove" alt="remove autostart" title="Der Service wird beim booten des Servers nicht gestartet. Dies muss nun manuell erfolgen.">Autostart deaktivieren</a>'; } else { echo 'Nein - <a href="?append_autostart='.trim($file).'" rel="add" alt="add autostart" title="Der Service wird beim booten des Servers automatisch gestartet.">Autostart aktivieren</a>'; } ?></span><br><?php } ?>
							<span class="header_item check_active_status" >
								<strong>Status: </strong>
								<font style="text-transform: capitalize; color:<?php if ($service_status_check == 'active') { echo 'green'; } else { echo 'red'; } ?>"><?php echo $service_status; ?></font> -
								<?php
									if ($service_status_check != 'active') {
										if(file_exists($service_verzeichnis.'/'.$file.'/docs/main.py')) {
								?>
									<a href="?start_service=<?php echo trim($file); ?>" rel="start" alt="start service" title="Der Service wird gestartet.">Service starten</a>
								<?php
										} else {
								?>
									<strong>main.py nicht vorhanden!</strong>
								<?php
										}
									} else {
								?>
									<a href="?stop_service=<?php echo trim($file); ?>" rel="stop" alt="stop service" title="Der Service wird gestoppt.">Service stoppen</a>
								<?php } ?>
							</span><br>
							<?php if (!empty($service_status_time)) { ?>
							<span class="header_item check_time_status"><strong>Seit: </strong><?php echo $service_status_time; ?></span><br>
						<?php } ?>
							<span class="header_item github"><strong>GitHub: </strong>
								<?php
									if (count(scandir($service_verzeichnis.'/'.$service_data[1].'/docs')) > 2) {
										if (!is_dir($service_verzeichnis.'/'.$service_data[1].'/docs/.git')) {
											echo 'Das Verzeichnis ist nicht leer.';
										} else {
											$key = hash('sha512', file_get_contents($service_verzeichnis.'/'.$service_data[1].'/.data.csv'));
											$github_repo_link = explode("\n", explode('url = ', file_get_contents($service_verzeichnis.'/'.$service_data[1].'/docs/.git/config'))[1])[0];
											if (array_reverse(explode('.', $github_repo_link))[0] != 'git') {
												$github_repo_webhook_link = $github_repo_link.'/settings/hooks/new';
											} else {
												$github_repo_webhook_link = str_replace('.git', '/settings/hooks/new', $github_repo_link);
											}
											$copy_value_rand = rand(999999, 9999999);
											?>
											<script>
												function copy<?php echo $copy_value_rand; ?>() {
														const el = document.createElement('textarea');
														el.value = "<?php echo $data['own_url'].'webhook.php?'.$key; ?>&service=1";
														document.body.appendChild(el);
														el.select();
														document.execCommand('copy');
														document.body.removeChild(el);
												}
											</script>
											<strong>Webhook Link</strong>
											<a onclick="copy<?php echo $copy_value_rand; ?>()" href="<?php echo $github_repo_webhook_link; ?>" target="_blank" style="cursor: pointer; display: inline-table; width: 280px;">
												<input type="text" value="<?php echo $data['own_url'].'webhook.php?'.$key; ?>&service=1" title="Gebe diesen Link unter <?php echo $github_repo_webhook_link; ?> ein. Empfohlen sind die vorgegebenen Einstellungen. Mit klick hierdrauf, wird der Link automatisch kopiert." style="cursor: pointer;" readonly>
												<small><i>Webhok Link kopieren und Einstellungen öffnen</i></small>
											</a>
											<?php
										}
									} else {
								?>
								<form method="post">
									<label for="inputRepository">
										<input type="text" name="service_repository" id="inputRepository" title="Trage hier ein Repository von der Plattform GitHub ein, um es zu klonen." alt="github repository" placeholder="https://github.com/nutzername/repository-name" maxlength="255" autocomplete="off" required>
									</label>
									<button type="submit" name="service_repository_button" value="<?php echo $file; ?>" title="Stelle eine Verbindung zum Repository her.">Klonen</button>
								</form>
								<?php
									}
								?>
								<p><?php if(isset($status)) { echo $status; } ?></p>
							</span><br>
						</div>
						<div class="third_header">
							<span class="header_item make_manually_backup"><?php if (count(scandir($service_verzeichnis.'/'.$file.'/docs')) > 2) { ?><a href="?make_manually_backup=<?php echo trim($file); ?>&service=1" rel="backup" alt="make manually backup" title="Mache ein manuelles Backup aller Verzeichnisinhalte des ./docs/ Ordners.">Backup machen</a><?php } else { ?><abbr title="In diesem Verzeichnis sind noch keine Dateien vorhanden, sodass auch kein Backup gemacht werden kann." class="prohibited_link">Backup machen</abbr><?php } ?></span>
							<span class="header_item delete_content"><?php if ('webservermanagementsystem' != $file) { ?><a href="?delete_domain=<?php echo trim($file); ?>" rel="delete" alt="delete site" title="Dieser Service wird mit allen Daten endgültig gelöscht. 𝘼𝙘𝙝𝙩𝙪𝙣𝙜, 𝙙𝙞𝙚𝙨𝙚𝙧 𝙑𝙤𝙧𝙜𝙖𝙣𝙜 𝙠𝙖𝙣𝙣 𝙣𝙞𝙘𝙝𝙩 𝙧ü𝙘𝙠𝙜ä𝙣𝙜𝙞𝙜 𝙜𝙚𝙢𝙖𝙘𝙝𝙩 𝙬𝙚𝙧𝙙𝙚𝙣. Mache sicherheitshalber vorher ein Backup.">Service & Inhalt löschen</a><?php } else { ?><abbr title="Dieser Service kann nicht gelöscht werden, da es sich um die Seite handelt, auf der diese Meldung gerade angezeigt wird. Wenn dieser Service gelöscht werden würde, würde gar nichts mehr funktionieren." class="prohibited_link">Service & Inhalt löschen</abbr><?php } ?></span>
						</div>
						</section>
				<?php
		}
	}
		closedir($handle_service);
	}
}
?>
		<section id="main_section">
			<div class="backup">
				<span class="backup_item backup_all"><a href="?make_manually_whole_backup=1" rel="backup" alt="make manually whole backup" title="Mache ein Backup von allen Seiten. Dabei wird jede Seite einzeln in eine Zip Datei verpackt.">Gesamtes Backup machen</a></span>
				<?php
					if (isset($data['mysql_username'])) {
				?>
				<span class="backup_item backup_all_dbs"><a href="?make_manually_whole_db_backup=1" rel="backup" alt="make manually whole db backup" title="Mache ein Backup von allen Datenbanken. Dabei wird jede einzelne Datenbank als SQL-Datei abgespeichert.">Datenbanken Backup machen</a></span>
			<?php } ?>
			</div>
			<div>
				<span class="list_element"><strong class="title">Interne IP-Adresse:</strong> <?php echo $_SERVER['SERVER_ADDR']; ?></span>
				<span class="list_element phpmyadmin_button"><a href="<?php echo $_SERVER['REQUEST_SCHEME'].'://'.'phpmyadmin.'.$data['domainname'] ?>" rel="external" alt="phpmyadmin" title="MySQL Datenbanken verwalten" target="_blank">phpMyAdmin</a></span>
				<span class="list_element"><strong class="title">Externe IP-Adresse:</strong> <?php echo $_SERVER['REMOTE_ADDR']; ?></span>
			</div>
			<div class="databases">
				<details class="database_details">
					<summary>Datenbank Zugangsdaten</summary>
					<form method="post">
						<label for="inputUsername">
							<input type="text" name="username" id="inputUsername" value="<?php echo $data['mysql_username']; ?>" title="Gebe den root Benutzernamen des MySQL Benutzers ein. Dieser wird dafür verwendet, um andere Benutzer zu erstellen und hier die Datenbanken zu verwalten." alt="mysql username" placeholder="MySQL-Benutzername (root)" maxlength="32" autocomplete="off" required>
						</label>
						<label for="inputPassword">
							<input type="password" name="password" id="inputPassword" title="Gebe das zugehörige MySQL-Passwort ein." alt="mysql password" placeholder="MySQL-Passwort" maxlength="32" autocomplete="off" required>
						</label>
						<button type="submit" name="mysql_login" title="Logge dich mit den MySQL Zugangsdaten ein.">Anmelden</button>
					</form>
					<?php
						if (isset($data['mysql_username'])) {
					?>
					<form method="post" class="unset db_logout">
						<button type="submit" name="mysql_logout" title="Lösche die MySQL Zugangsdaten.">Abmelden</button>
					</form>
				<?php } ?>
				</details>
				<details class="config_password_details">
					<summary>Config Passwort</summary>
					<form method="post">
						<label for="inputPassword">
							<input type="password" id="inputPassword" name="password" title="Passwort zum einloggen der Config Seite" alt="password" placeholder="Passwort der Config Seite" autocomplete="off" maxlength="32" required>
						</label>
						<button type="submit" name="change_config_password" title="Speichere das neue Passwort ab.">Speichern</button>
					</form>
				</details>
			</div>
		</section>
		<form method="post" id="newsubdomain">
			<label for="inputSubname">
				<input type="text" id="inputSubname" name="domainname" placeholder="Domain Name (z.B. sub.example.com)" pattern="[abcdefghijklmnopqrstuvwxyz0123456789\-.]+" title="Bitte verwende nur Kleinbuchstaben und Zahlen und maximal ein Minuszeichen, welches sich nicht an der ersten, dritten, vierten oder letzten Stelle befindet." maxlength="40" required>
			</label>
			<label for="inputMail">
				<input type="email" id="inputMail" name="mail" placeholder="E-Mail-Adresse" value="<?php echo trim($_COOKIE['mail']); ?>" pattern="^[\w\.\+\-]+\@[\w\-]+\.[a-z]{2,3}$" title="Bitte gebe eine gültige E-Mail-Adresse an." minlength="6" maxlength="120" required>
			</label>
			<label for="inputRedirect">
				<input type="checkbox" id="inputRedirect" name="redirect" checked> Automatische <i>https://</i> weiterleitung
			</label>
			<button type="submit" name="newdomain">Neue Domain erstellen</button>
		</form>
		<hr>
		<form method="post" id="newservice">
			<p>
				Es wird ein Service erstellt, der das <strong>main.py</strong> Python3-Script des jeweiligen Verzeichnises startet.
			</p>
			<label for="inputServicename">
				<input type="text" id="inputServicename" name="servicename" placeholder="Service Name" pattern="[abcdefghijklmnopqrstuvwxyz0123456789]+" title="Bitte verwende nur Kleinbuchstaben und Zahlen." maxlength="40" required>
			</label>
			<label for="inputAutostart">
				<input type="checkbox" id="inputAutostart" name="autostart"> Automatischer Start des Services bei Systemstart.
			</label>
			<button type="submit" name="newservice">Neuen Service erstellen</button>
		</form>
	</section>
	<section id="main">
		<?php if (isset($msg_field)) { echo $msg_field; } ?>
		<?php
			require('./inc/webssh.inc.php');
		?>
	</section>
<?php
}
	require('./inc/footer.inc.php');
?>
