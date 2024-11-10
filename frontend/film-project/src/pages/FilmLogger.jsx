import Header from "./components/Header"
import {Modal, ModalContent, ModalHeader, Input, ModalBody, DateInput, Textarea, Button} from "@nextui-org/react"
export default function FilmLogger()
{
    return(
        <div className="w-[100vw] h-[100vh] z-10">
            <Header className="absolute top-[0px]"/>
            <div className="w-[100vw] h-[100vh] fixed top-[0px] flex justify-center items-center">
            <div className="relative w-[80vw] h-[80vh] inline-block rounded-[30px] shadow-lg bg-[#202020]">
                    <div className="Header w-[100%] ml-[50px] mt-[50px] mb-[50px]">
                        <h1 className="font-semibold text-white text-[30px]">Add a Film</h1>
                    </div>
                    <img src="https://placehold.co/2000x3000" className="absolute ml-[50px] w-[200px] rounded-[15px]"></img>
                    <div className="InputFields ml-[290px] mr-[20px]">
                        <Input className="mb-[10px]"placeholder="Film Name"></Input>
                        <DateInput className="mb-[10px]"placeholder="Watch Date"></DateInput>
                        <Textarea className="min-h-[300px]" placeholder="Write a review!"></Textarea>
                    </div>
                    <div className="absolute bottom-[20px] right-[50px]">
                        <Button className="mr-[20px]">Cancel</Button>
                        <Button className="">Submit</Button>
                    </div>
            </div>
        </div>
        </div>
        
    );
}