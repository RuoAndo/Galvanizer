import akka.actor._
import scala.collection.mutable.ListBuffer

case class MapCompleted()
case class ReduceCompleted()

/*
class MasterActor(mapActors: Array[Actor],
                  reduceActors:Array[Actor],
                  data: List[String]) extends Actor{
*/
class MasterActor extends Actor {

  import context._

  val mapOutputs = new ListBuffer[MapOutput]
  val reduceInputs = new ListBuffer[ReduceInput]
  val reduceOutputs = new ListBuffer[ReduceOutput]

  // メッセージハンドラとなるメソッド
  def receive = {
    /*
    case s: String => subref ! s		        // 子のアクターへ送信
    case Terminated(subref) => println("SubActor終了")	// 子のアクターの終了時
    */
    case _ => println("unknown")
  }
}