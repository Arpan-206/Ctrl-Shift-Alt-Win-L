import Header from "./components/Header";
import {Card, CardBody, Spacer, Image} from "@nextui-org/react"
import {useState, useEffect} from "react"
import GetDiscoveryData from "../API/Discovery";
export default function Discovery()
{
    const [data, setData] = useState(["data", "setData"]);
    useEffect(() => {
        GetDiscoveryData().then(respone=>{
            setData(respone);
            console.log(response);
        })
        
    }, []);
    return(
        
        <div className="absolute top-[0px] w-[100vw] h-[100vh] ">
            <Header></Header>
            <div className="block">
                <h1 className = "text-[50px] w-[100vw]">Discovery</h1>
                {data!=null && data.map((item, index) => {
                    return(
                        <div>
                        <Card className="relative w-[80%] left-[10%] mb-[40px] opacity-10 bg-white">
                            <CardBody className="h-[300px]">
                                <h3 className="text-[50px] text-center">{item.Title}</h3>
                                <span>
                                    <Image src={item["Poster"]} className= "w-[300px]"></Image>
                                    <h3 className="text-[25px]">
                                        {item.Reason}
                                    </h3>
                                </span>
                            </CardBody>
                        </Card>
                        <Spacer></Spacer>
                        </div>
                    )
                })}
                
                </div>
            </div>
    );
}