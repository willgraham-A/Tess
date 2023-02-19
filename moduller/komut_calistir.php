$komut = "_COMMAND";

$cikti = shell_exec($komut);
if (empty($cikti)){
    echo `$komut`;
} else {
    echo $cikti;
}

