<?php

function color($color, $text)
{
    $arrayColor = array(
        'grey'      => '1;30',
        'red'       => '1;31',
        'green'     => '1;32',
        'yellow'    => '1;33',
        'blue'      => '1;34',
        'purple'    => '1;35',
        'nevy'      => '1;36',
        'white'     => '1;0',
    );  
    return "\033[".$arrayColor[$color]."m".$text."\033[0m";
}
function curlBoss($url, $data=NULL, $headers = NULL) {
    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    if(!empty($data)){
        curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    }

    if (!empty($headers)) {
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    }

    $response = curl_exec($ch);

    if (curl_error($ch)) {
        trigger_error('Curl Error:' . curl_error($ch));
    }

    curl_close($ch);
    return $response;
}


echo color('blue', "[+]") . " =============================\n";
echo color('blue', "[+]") . " Checker Name Game | By RenJul\n";
echo color('blue', "[+]") . " =============================\n";
echo color('blue', "[+]") . " 1. Free Fire (Player ID)\n";
echo color('blue', "[+]") . " 2. Mobile Legend (UserID_ServerID)\n";
echo color('blue', "[+]") . " 3. Bigo Live (Player ID)\n";
echo color('blue', "[+]") . " 4. COD Mobile (Open ID) \n";
echo color('blue', "[+]") . " 5. King Of Kings (Role Number) \n";
echo color('blue', "[+]") . " 6. AOV (Player ID) \n";
echo color('blue', "[+]") . " 7. HAGO (User ID)\n";
echo color('blue', "[+]") . " 8. VALORANT (Riot ID) \n";
echo color('blue', "[+]") . " 9. Crisis Action (AccountID_ServerID) \n";
echo color('blue', "[+]") . " 10. Game Of Sultan (UserID) \n";
echo color('blue', "[+]") . " 11. Love Nikki (UserID) \n";
echo color('blue', "[+]") . " 12. Genshin Impact (UserID_ServerID) \n";
echo color('blue', "[+]") . " 13. Life After (UserID_ServerID)\n";
echo color('blue', "[+]") . " 14. Ragnarok M (UserID_ServerID)\n";
echo color('blue', "[+]") . " 15. Leagua Of Legend (Riot ID)\n";
echo color('blue', "[+]") . " 16. Point Blank Bayond (Username) \n";
echo color('blue', "[+]") . " 17. Higgs Domino Coins (User ID)\n";
echo color('blue', "[+]") . " =============================\n";
echo color('blue', "[+]") . " Silahkan pilih: ";
$id = trim(fgets(STDIN));
if($id > 0 AND $id <= 17) {
    try {
        echo color('blue', "[+]") . " User ID : ";
        $user_id = trim(fgets(STDIN));
        $data = "id=$id&data=$user_id";
        $result = json_decode(curlBoss('http://beliscript.com/apiCheckGame.php?'.$data.''));
        if($result->status) {
            echo color('green', "[+]") . " Name : ".$result->data->name." ";

        } else {
            echo color('red', "[-]") . " Error :".$result->message." ";  
        }
     
    } catch (\Throwable $th) {
        echo color('red', "[-]") . " ".$th->getMessage()." ";
    }
} else {
    echo "Id Tidak Tersedia \n";
}





?>