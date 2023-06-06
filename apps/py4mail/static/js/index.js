let app = {};

let init = (app) => {
  // This is the Vue data.
  app.data = {
    emails: [],
    emails_as_dict: {},
    mailOption: 0, // 0 = list, 1 = individual mail
    mail: {}
  };

  app.enumerate = (a) => {
    // This adds an _idx field to each element of the array.
    let k = 0;
    a.map((e) => {
      e._idx = k++;
    });
    return a;
  };

  // This contains all the methods.
  app.methods = {
    formatEmailsByTime: function () {
      app.vue.emails.sort(function (a, b) {
        return new Date(b.sent_at) - new Date(a.sent_at);
      });
    },

    //One function that get the information for the three different types of mails
    //param of `type` to get the mails from inbox, trash, or starred
    getGlobal: function(type, isType) {
      app.vue.mailOption = 0;
      axios.get(get_emails_url).then(function(response) {
        app.vue.emails = app.enumerate(response.data.emails).filter(function(email) {
          if (email[isType] === type) {
            return true;
          }
          return false;
        });
        app.methods.formatEmailsByTime();
      });
    },

    //get the mails from inbox
    getInbox: function() {
      app.methods.getGlobal(null, 'isTrash');
    },    
    getSent: function() {
      app.vue.mailOption = 2;
      axios.get(get_sent_url).then(function(response) {
        app.vue.emails = app.enumerate(response.data.emails);
        app.methods.formatEmailsByTime();
      });
    },
    //get the mails from trash
    getTrash: function() {
      app.methods.getGlobal(true, 'isTrash');
    },

    //get the mails from starred
    getStarred: function() { 
      app.methods.getGlobal(true, 'isStarred');
    },

    // view individual mail 
    viewMail: function(email_id) {
      app.vue.mailOption = 1; //switch to individual mail
      app.vue.mail = email_id;
    },
    compose_mail: function(email) {
      console.log(email);
      // use the api to send the email
      axios
      .post(get_compose_url, { email: { receiver_mail: email.receiver_mail, title: email.title, content: email.content } })
      .then(function(response) {
        if (response.data === "Mail sent successfully") {
          app.methods.getInbox();
        }      
      })
      .catch(function(error) {
        console.error(error);
      });
    },
    // trash or delete the email
    trashOrDeleteMail: function(email_id) {
      app.vue.emails.forEach(function(email){
        if (email.id === email_id) {
          if (email.isTrash === true) {
            axios.post(delete_url,
              {
                id: email.id,
              }).then(function(response) {
                app.vue.emails.splice(app.vue.emails.indexOf(email), 1);
                delete app.vue.emails_as_dict[email];
              });
          } else {
            axios.post(trash_url,
              {
                id: email.id,
              }).then(function(response) {
                app.vue.emails.indexOf(email).isTrash = true;
              });
          }
        }

      });
      
    },
    starMail: function(email_id) {
      axios.post(star_url,
        {
          id: email_id,
        }).then(function(response) {
          app.vue.emails.forEach(function(email){
            if (email.id === email_id) {
              new_email = email;
              if (email.isStarred === true) {
                new_email.isStarred = false;
              } else {
                new_email.isStarred = true;
              }
              app.vue.emails.splice(app.vue.emails.indexOf(email), 1);
              app.vue.emails.push(new_email);
            }
          });
        });
    },
  };

  // This creates the Vue instance.
  app.vue = new Vue({
    el: "#vue-target",
    data: app.data,
    methods: app.methods,
  });

  // And this initializes it.
  app.init = () => {
    //get mails from inbox by default
    app.methods.getInbox();
  };

  // Call to the initializer.
  app.init();
  
  const composeButton = document.getElementById('composeButton');
  const modal = document.getElementById('modal');
  const receiver_mail = document.getElementById('address');
  const title = document.getElementById('subject');
  const emailContent = document.getElementById('emailContent');
  const sendButton = document.getElementById('sendButton');
  
  // show the email form
  composeButton.addEventListener('click', () => {
    modal.style.display = 'block';  // show the form
  });
  // call compose_email to send the email
  sendButton.addEventListener('click', () => {
    // get the content for the email
    let email = {};
    email.receiver_mail = receiver_mail.value;
    email.title = title.value;
    email.content = emailContent.value;

    // Reset the fields
    receiver_mail.value = '';
    title.value = '';
    emailContent.value = '';
    modal.style.display = 'none'; // hide the form
    app.methods.compose_mail(email);
  });

  closeMail.addEventListener('click', () => {
    // reset the field
    receiver_mail.value = '';
    title.value = '';
    emailContent.value = '';
    modal.style.display = 'none';   // hide the form
  });
};

// This takes the (empty) app object, and initializes it,
// putting all the code in it.
init(app);

