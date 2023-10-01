
<iframe width="560" height="315" src="https://www.youtube.com/embed/nZ7r-A4vi4w?si=bEtyqH3wm680zr4H" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
https://youtu.be/nZ7r-A4vi4w

```python
import fast

fast.data.appVersion = "0.0.7"
fast.data.appName = "Awesome PyPi package5"
fast.data.appDescriptionShort = "my short description"
fast.data.appReadme = "my app's README.md"
fast.data.license = "my app's license"
fast.data.developers =[fast.data.Developer("Olliver Aira", contactInformation={"email": "olliver.aira@gmail.com"})]
fast.devTools.uploadModuleToPypi('./myProjectThatIWantUploaded', testPypi=True)#@note set testPypi=False if you're uploading a permanent package for a real project
```