
import { useState } from "react";
import { useEffect } from "react";

function Search(this: any) {

   function handleInputChange(event:any){
        var [input_data, setSearch] = useState( "")
        useEffect(()=>{
            console.log("call effect")
        }, [])
        event.preventDefault()
        setSearch(input_data = event.target.value)
   }
   function handleSubmit(event:any){
        event.preventDefault()
        const formdata:any = new FormData(event.target)
    }

    return(
        <div className="login">
            <form action="" onSubmit={handleSubmit}>
                <input type="search" name="search_input" id="search_input" placeholder="Search for dots" onChange={handleInputChange} ref={this.input_data}/>
                <button type="submit"><img src="" alt="Search" /></button>
            </form>
        </div>
    )  
};


export default Search;
