$(document).ready(function() {
    $('#registration-form')
    .formValidation({
       framework: 'bootstrap',
	   icon: {
	       valid: 'glyphicon glyphicon-ok', 
	       invalid: 'glyphicon glyphicon-remove',
	       validating: 'glyphicon glyphicon-refresh'
	   },
           fields: {
	       first_name: {
	           validators: {
		       notEmpty: {
		            message: 'Please provide a first name' 
		       }, 
		       regexp: {
		            regexp: /^[A-z]+$/, 
		            message: 'Only alphabetic characters are allowed' 
		       }
		   } 
	       }, 
	       middle_name: {
		   enabled: false,
	           validators: {
		       notEmpty: {
		            message: 'Please provide a first name' 
		       }, 
		       regexp: {
		            regexp: /^[A-z]+$/, 
		            message: 'Only alphabetic characters are allowed' 
		       }
		   } 
	       
	       }, 
	       surname: {
	           validators: {
		       notEmpty: {
		            message: 'Please provide a surname' 
		       }, 
		       regexp: {
		            regexp: /^[A-z]+$/, 
		            message: 'Only alphabetic characters are allowed' 
		       }
		   } 
	       
	       }, 
	       email_address: {
	           validators: {
		       notEmpty: {
		            message: 'An email address is required' 
		       },
		       emailAddress: {
		            message: 'That is not a valid email address' 
		       }
		   } 
	       
	       }, 
	       id_number: {
	           validators: {
		       notEmpty: {
		            message: 'Your ID number is required' 
		       },
		       regexp: {
		            regexp: /^(ENG|ABS|ADS)\d{2}[AB]\d{5}Y/i, 
		            message: 'That is not a valid ID number' 
		       },
		       blank: {
		       }
		   } 
	       }, 
	       phone_number: {
	           validators: {
		       notEmpty: {
		            message: 'Your phone number is required' 
		       },
		       regexp: {
		            regexp: /^(\+233|0)\d{9}\d*$/, 
		            message: 'That is not a valid phone number'
		       },
		   } 
	       }, 
	       password_confirm: {
	           validators: {
		        verbose: false,
		       identical: {
			      field:'password',
		            message: 'Please enter matching passwords' 
		       }
		   } 
	       
	       }, 
	       password: {
	           validators: {
		       verbose: false,
		       notEmpty: {
		            message: 'Please provide a password' 
		       }
		   } 
	       
	       }, 
	       program: {
	           validators: {
		       notEmpty: {
		            message: 'Please choose one program' 
		       }
		   } 
	       }
	   }, 
    
    })
})

