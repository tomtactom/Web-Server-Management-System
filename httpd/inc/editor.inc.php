<?php
  // open this directory
  $myDirectory = opendir("../../config.".$data['domainname']."/httpd");

  // get each entry
  while($entryName = readdir($myDirectory)) {
  	$dirArray[] = $entryName;
  }

  // close directory
  closedir($myDirectory);

  //	count elements in array
  $indexCount	= count($dirArray);
  Print ("$indexCount files<br>\n");

  // sort 'em
  sort($dirArray);

  // print 'em
  print("<table>");
  print("<tr><th>Dateiname</th><th>Dateityp</th><th>Größe</th></tr>");
  // loop through the array of files and print them all
  for($index=0; $index < $indexCount; $index++) {
    if (substr("$dirArray[$index]", 0, 1) != "."){ // don't list hidden files
  		print("<tr><td><a href='".explode('&', $data['own_url_with_get'])[0]."&dir=".$dirArray[$index]."'>".$dirArray[$index]."</a></td>");
  		print("<td>");
  		print(filetype($dirArray[$index]));
  		print("</td>");
  		print("<td>");
  		print(filesize($dirArray[$index]));
  		print("</td>");
  		print("</tr>");
  	}
  }
  print("</table>");
?>
