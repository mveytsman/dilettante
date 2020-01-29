# Dilettante 

More information on my blog [here](http://blog.ontoillogical.com/blog/2014/07/28/how-to-take-over-any-java-developer/)

It turns out that [Maven Central](http://search.maven.org/) only lets you use SSL if you purchase an authentication token for a [donation](http://www.sonatype.com/clm/secure-access-to-central) of $10. They claim this $10 will go to the Apache project, but that's besides the point.

SSL encryption requires a separate authentication token. To see what I mean, try opening  [http://central.maven.org/maven2/org/springframework/](http://central.maven.org/maven2/org/springframework/) and [https://central.maven.org/maven2/org/springframework/](https://central.maven.org/maven2/org/springframework/) in your browser. This means that package managers like Clojure's lein, Scala's sbt, and maven itself when not specially configured will download JARs without any SSL. 

Dilettante is a man in the middle proxy that injects malicious codes into JARs served by Maven Central.

## Usage


1. Get in a position where you can man-in-the-middle HTTP traffic. Some hints:
   - Buy a wifi router, call it "Starbucks Wifi"
   - Install [ettercap](https://ettercap.github.io/ettercap/)
   - Happen to be an ISP
   - Something something 

2. Run `dilettante.py`
3. Proxy your target's http traffic through `localhost:8080`
   - You can do an easy PoC of this by setting the `<proxy>` setting in `~/.m2/settings.xml`

## Results
Your victims will get a friendly image when they execute any Java code that uses a JAR that passed through dilettante.
![screenshot](media/screen.png)

You can see a video [here](media/screencast.mp4)
