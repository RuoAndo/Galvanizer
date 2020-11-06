// package chap09.program06
// import scala.actors._
// import scala.actors.Actor._

import akka.actor.Actor
import akka.actor.{ActorSystem,Props}

class ReduceActor extends Actor{
  def act() {
    println("ReduceActor: Starting...")
    loop {
      react {
        case i: ReduceInput => reply(reduce(i))
        case _ => println("ReduceActor: ???")
      }
    }
  }
  def reduce(i: ReduceInput) = {
    ReduceOutput(i.key, i.entries.foldLeft(0)(_ + _._2))
  }
}
