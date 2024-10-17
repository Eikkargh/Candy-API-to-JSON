# Candy-API-to-JSON

This python script is designed to communicate with Candy/Hoover washer dryers to produce a JSON readable by Home Assistant.<br><br>
Tested and working on:
<ul>
  <li>Hoover WDWOA596H WIFI Washer Dryer</li>
  <li>Hoover H3DS4965TACBE-80 Washer Dryer</li>
</ul>

<h2>Getting the API Key</h2>
To obtain the key for the machine I used: <a href=https://github.com/Alamot/code-snippets/blob/master/crypto/xorknown.py>xorknown.py</a> from: <a href=https://github.com/Alamot>@Alamot.</a>
For most reliable responses, getting the key should be done while the machine is running a program. 
<br><br>
<ol>
  <li>In a terminal run the command:<br>
      <code>curl -s http://CANDY_IP/http-read.json?encrypted=1 | xxd -r -p > ./coded.txt</code><br>
      This gets the raw hex data from the machines API and converts to plaintext. </li>
  <br>
  <li>Feed the coded.txt into xorknown.py using:<br>
      <code>./xorknown.py ./coded.txt '{"statusLavatric' 16</code></li>
  <br>
  <li>the output should now contain a key of length 16 and a JSON. An example decoded JSON:<br>
      <pre><code>Plaintext: {
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
  }</code></pre></li>
  <br>
  <li>If you do not have a full key at this stage repeat step 3 using another JSON key value like 'WiFiStatus' until each character of the key is known.</li>
  <br>
  <li>Add your KEY and DEVICE_IP to candy.py and place in your Home Assistant config/pyscripts.</li>
</ol>
<br>
<h2>Configuring Home Assistant</h2>
candy.py gets the data, decodes it and strips down the JSON to meet Home Assistants 255 character limit on sensors.<br>
To set up in Home Assistant you can use the sensor:<br>
<pre><code>
command_line:
  - sensor:
      name: 'Candy Washer Dryer'
      scan_interval: 60
      command_timeout: 30
      command: python3 ./pyscript/candy.py
      value_template: '{{ value_json }}'
      json_attributes:
        - WiFiStatus
        - Err
        - MachMd
        - Pr
        - PrPh
        - Temp
        - SpinSp
        - RemTime
        - DryT
        - DelVal
        - TotalTime
</pre></code>
This may be different on some machines. Yaml exmaples for test machines are above. If your machine is not listed please raise an issue with a copy of your decoded output. <br>
<img src=https://user-images.githubusercontent.com/87714048/216792725-cd230740-77ca-4f6e-9c5c-08257d17a7e0.png alt="candy-card">

<ul><li>example templates including translations of machine program codes can be found in configuration.yaml. </li>
    <li>example cards can be found in lovelace.yaml. These use <a href="https://github.com/thomasloven/lovelace-card-mod">custom:card-mod</a>, <a href="https://github.com/thomasloven/lovelace-fold-entity-row">custom:fold-entity-row</a> and <a href="https://github.com/iantrich/config-template-card">custom:config-template-card</a> integrations.</li>
</ul>

