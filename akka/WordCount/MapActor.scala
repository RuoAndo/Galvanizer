// package chap09.program06
//import scala.actors._
// import scala.actors.Actor._

import scala.collection.mutable.ListBuffer

import akka.actor.Actor
import akka.actor.{ActorSystem,Props}


class MapActor extends Actor{

    def receive = {
    	case s: String => reply(map(text))
	case _ => println("MapActor: ???")
    }
  
  def map(text: String) = {
    val words = new ListBuffer[(String, Int)]
    text.split(' ').foreach(words += _->1)
    MapOutput(words.toList)
  }
}
