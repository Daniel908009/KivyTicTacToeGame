# kivy_tic_tac_toe
## What is it?
<p>This project is a Tic Tac Toe game build in Kivy(multiplatform, naturaly resizable framework), with computer enemy.</p>

## Features
<p>Fully customizable grid.</p>
<p>Settings window(custom size of the grid, custom number of tiles in line needed for winning).</p>
<p>Play mode against AI. (currently not very smart, but it works)</p>

## Screenshots
![image](https://github.com/user-attachments/assets/6018728b-2674-41b5-b221-49fd09ed4024)
![image](https://github.com/user-attachments/assets/43363aa6-0373-41df-a4c4-7cbef61d2cda)
![image](https://github.com/user-attachments/assets/46afd279-0fae-4100-b096-eb92afeaa82e)

## To do
[X] Layout of the app<br>
[X] Clickable button grid<br>
[X] Winner conditions checking<br>
[] AI opponent(Something of a prototype done)<br>

## AI explanation
<p>Currently the AI recognizes if player can win and blocks him, and it recognizes if it can win in one move. However it cant think more than one move ahead.</p>
<p>A part of the algorithm for thinking ahead is in the code, however it isnt completed yet, since this is the first time I am doing recursive functions.</p>
<p>Update: I had to rework the entire enemy control twice now, however this version seems very close to working. But there is something wrong with the final results that it gives. For some reason all buttons have the same priority rating no matter what, for example they all have priority of 80000 or 20000 or something like 5000, possible reasons include wrong switching of players or badly done priority rating based on depth.</p>
<p>Will have to look into it, but one thing is certain. I do not like recursive functions.</p>
<p>*Note I would not recommend to play the game in its current state. However if you still want to play it, you will need to change to player VS player in the settings popup inside the app (you can see the opening button in the screenshots)</p>

<h1>Download instructions</h1>
*Note the links are instructional images <br>
**Note the images used bellow are from a different Github repository, however the overall procces is allways the same. <br>
<h2>Using graphic UI</h2>
<h3>Downloading source code </h3>
First click on the code button as shown in the picture bellow, then click the option Download ZIP <br>
(https://github.com/user-attachments/assets/801a8deb-b6e5-475e-9b6b-262b56fd6a23) <br>
After its downloaded you can find it on your computer through file explorer. After you have found it right click it, it should display option called "Extract" <br>
Click on it and wait a moment. A new directory should appear containing all the files neccesary for the game.<br>
Now open a console and enter the folowing code: pip install -r /path/to/requirements.txt <br>
*Replace the /path/to/requirements.txt with the actual path. <br>
Enjoy! <br>
<h2>Using command prompt</h2>
<h3>Downloading source code </h3>
Open your command prompt and enter the folowing code without the " letters <br>
"https://github.com/Daniel908009/Kivy_Tic_Tac_Toe_Game" <br>
This code adress of the site can also be found if you click the code button inside the github repository UI <br>
If you dont have git than first enter the folowing command: sudo apt install git <br>
Now open a console and enter the folowing code: pip install -r /path/to/requirements.txt <br>
*Replace the /path/to/requirements.txt with the actual path. <br>
Enjoy! <br>
<h2>Using Pypi</h2>
simply open your command prompt and enter this command: pip install kivy-tic-tac-toe-package <br>
then you can run it with this command: kivy_tic_tac_toe_package
