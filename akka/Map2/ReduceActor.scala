import akka.actor.Actor
import akka.actor.{ActorSystem,Props}

class ReduceActor extends Actor{

  def receive = {
        case i: ReduceInput =>
	     println("ReduceActor received")
	     println(reduce(i))
        case _ => println("ReduceActor: ???")
	
  }
  def reduce(i: ReduceInput) = {
    ReduceOutput(i.key, i.entries.foldLeft(0)(_ + _._2))
  }
}
