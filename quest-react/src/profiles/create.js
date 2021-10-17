
import React, {Component} from 'react'
import { apiRegistry } from './lookup'


export class RegUsr extends Component{

  constructor () {
    super()
    this.state = {
      fname: "",
      cont: "",
      conTyp: "email",
      email: true,
      pwd: "",
      pwd2: ""
    };

    this.checkContact = this.checkContact.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this)
  }

  handleChange(event) {
    this.setState({
      [event.target.name]: event.target.value
    });
  }
  
  handleBackendUpdate (response, status){
    if (status === 201){
      console.log(response)
    } else {
      console.log(response)
      alert("An error occured please try again")
    }
  }

  checkContact (event) {
    const emel = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    //const numb = '[+,0-9]'
    if (!event.target.value.match(emel)) {
      this.setState({conType: "phone"})
      this.setState({email: false})
    }
    this.setState({
      [event.target.name]: event.target.value
    });
  }

  handleSubmit (event) {
    event.preventDefault()

    const { fname, cont, email, pwd, pwd2 } = this.state;
    const newUsr = {fname: fname, cont: cont, typ: email, pwd: pwd, pwd2: pwd2};

    // backend api request
    apiRegistry(newUsr, this.handleBackendUpdate)

    this.setState = {
      contact_type: "email",
      fullname: "",
      contact: "",
      password: "",
      verify_password: ""
    }
  }

  render() {
    return (
      <div>
        <form onSubmit={this.handleSubmit}>
          <input required
            type="text"
            name="fname"
            placeholder="Enter your full name"
            value={this.state.fname}
            onChange={this.handleChange}
          />
  
          <input required
            type={this.state.conTyp.toString()}
            name="cont"
            placeholder="Enter phone or E-mail"
            value={this.state.cont}
            onChange={this.checkContact}
          />
  
          <input required
            type="password"
            name="pwd"
            placeholder="Enter a new Password"
            value={this.state.pwd}
            onChange={this.handleChange}
          />
  
          <input required
            type="password"
            name="pwd2"
            placeholder="Confirm your password"
            value={this.state.pwd2}
            onChange={this.handleChange}
          />
  
          <button type="submit">Register</button>
        </form>
      </div>
    );
  } 
}
