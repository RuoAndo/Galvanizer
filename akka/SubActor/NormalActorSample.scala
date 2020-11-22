//package jp.sf.amateras.scala.akka

import akka.actor._
import scala.collection.mutable.ListBuffer

case class MapOutput(val entries:List[(String, Int)])
case class ReduceInput(val key:String, val entries:List[(String, Int)])
case class ReduceOutput(val key:String, val value:Int)
case class Begin()

case class MapCompleted()
case class ReduceCompleted()


/**
 * アクターを使った並行処理のサンプルです。
 */
class MainActor extends Actor with ActorLogging {
  import context._

  val mapOutputs = new ListBuffer[MapOutput]
  val reduceInputs = new ListBuffer[ReduceInput]
  val reduceOutputs = new ListBuffer[ReduceOutput]

  // メッセージハンドラとなるメソッド
  def receive = {
  /*
      case s: String => 
            val words = new List[(String)]
	    s.toString.split(' ').foreach(words += _->1)
	    map(0, words)
*/

    // case s: String => subref ! "msg to subactor" // 子のアクターへ送信
    // case s: String => MapRef ! s // 子のアクターへ送信
    //case mo: MapOutput => println("MapOutput received:" + mo)

         // appendMapOutput(mo); checkMapProgress
    	 // println(sort(mo.toList))

    // case MapCompleted =>
    	 // println("MapCompleted")

    // case Terminated(MapRef) => println("MapActor終了")
    // case Terminated(subref) => println("SubActor終了")	// 子のアクターの終了時
    case _ => log.warning("unknown")
  }

  def appendMapOutput(o: MapOutput) = {
    println("MasterActor: received the response: map(" + o + ")")
    mapOutputs += o
  }

  def checkMapProgress =
    if (mapOutputs.length > 10) sender ! MapCompleted
}

/**
 * Main
 */
object NormalActorSample extends App {
  val system = ActorSystem()

  val data = List("Hello World",
                  "Hello Scala World",
                  "Hello Java World",
                  "Hello Java Hello",
                  "Hello Scala Scala",
                  "Scala World World World",
                  "Scala World Scala World",
                  "Hello Groovy")

  // アクターの生成
  val ref = system.actorOf(Props[MainActor], name = "mainActor")
  // ref ! "send message"
  
  val MapRef = system.actorOf(Props[MapActor], name = "MapActor")
  // watch(MapRef)

  var str:String = ""
  for(element<-data) 
    str = str + element + " "

  println("Main actor:" + str)
  ref ! str

  map(0, data)

  def map(index: Int, data:List[String]) {
    data match {
      case Nil =>
      case x::xs => println("map:" + x)
		    MapRef ! x
                    map(index+1, xs)
    }
  }

  Thread.sleep(3000)
  // すべてのアクターを終了
  system.terminate()
}