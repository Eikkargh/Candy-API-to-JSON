# Candy-API-to-JSON

This python script is designed to communicate with Candy/Hoover washer dryers to produce a JSON readable by Home Assistant.

<h2>Getting the API Key</h2>
To obtain the key for the machine I used: <a href=https://github.com/Alamot/code-snippets/blob/master/crypto/xorknown.py>xorknown.py</a> from: <a href=https://github.com/Alamot>@Alamot</a>
For most reliable responses, getting the key should be done while the machine is running a program. 
<br><br>
<ol>
  <li>In a terminal run the command:<br>
      <code>curl -s http://<CANDY_IP>/http-read.json?encrypted=1 | xxd -r -p > ./coded.txt</code><br>
      This pulls the raw hex data from the machines API and converts to plaintext. </li>
  <br>
  <li>Feed the coded.txt into xorknown.py using:<br>
      <code>./xorknown.py ./coded.txt '{"statusLavatric' 16</code></li>
  <br>
  <li>the output should now contain a key of length 16 and a JSON like the bellow example:<br>
      <code>Plaintext: {
        "statusLavatrice":{
                "WiFiStatus":"0",
                "Err":"255",
                "MachMd":"1",
                "Pr":"4",
                "PrPh":"0",
                "SLevel":"255",
                "Temp":"60",
                "SpinSp":"10",
                "Opt1":"0",
                "Opt2":"0",
                "Opt3":"0",
                "Opt4":"0",
                "Opt5":"0",
                "Opt6":"0",
                "Opt7":"0",
                "Opt8":"0",
                "Steam":"0",
                "DryT":"0",
                "DelVal":"255",
                "RemTime":"59",
                "RecipeId":"0",
                "CheckUpState":"0"
        }
  }</code></li>
  <br>
  <li>If you dont not have a full key at this stage repeat
</ol>
