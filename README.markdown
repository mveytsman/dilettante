# Dilettante

It turns out that [maven central](http://search.maven.org/) only lets you use SSL if you purchase an authentication token for a [donation](http://www.sonatype.com/clm/secure-access-to-central) of $10. They claim this $10 will go to the Apache project, but that's besides the point.

SSL encryption requires a separate authentication token. To see what I mean, try opening  [http://central.maven.org/maven2/org/springframework/](http://central.maven.org/maven2/org/springframework/) and [https://central.maven.org/maven2/org/springframework/](https://central.maven.org/maven2/org/springframework/) in your browser. This means that package managers like Clojure's lein, Scala's sbt, and maven itself when not specially configured will download JARs without any SSL. 

dilettante is a script for [mitmproxy](http://mitmproxy.org/) that allows you to man in the middle JARs as they are downloaded form maven central. Currently, it will replace clojure.jar with a backdoored version that shows you a nice picture every time you run a clojure script
![h4x0r3d](screenshot.png)

