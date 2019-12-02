context('Connect', () => {
  beforeEach(() => {
    cy.visit('http://localhost:3000/login')
  });
  it('Fails to connect', () => {
    cy.get('#normal_login_username')
      .type('fake@email.com').should('have.value', 'fake@email.com');

    cy.get('#normal_login_password')
      .type('fake');
    cy.contains('Log in').click().wait(1000);
    cy.on('window:alert', (str) => {
        expect(str).to.equal(`Email Or Password Incorrect`)
    });
  });
  it('Success to connect', () => {
    cy.get('#normal_login_username')
      .type('admin@admin.com');
    cy.get('#normal_login_password')
      .type('admin');
    cy.contains('Log in').click();
    cy.on('window:alert', () => {
        expect(true).to.be.false;
    });
    cy.url().should('include', '/homeAdmin?show=All');
  });
});

// TODO CREATE USER random.mail@google.com random
context('Manage users Administrator', () => {
  beforeEach(() => {
    cy.visit('http://localhost:3000/login');
    cy.get('#normal_login_username')
        .type('admin@admin.com');
    cy.get('#normal_login_password')
        .type('admin');
    cy.contains('Log in').click().wait(200);
  });

  it('.creates user', () => {
    cy.visit('http://localhost:3000/users');
    cy.get(".User").its("length").then(numUsers => {
      cy.get('.anticon-plus').click();
      cy.get("#NewUserEmail").type("random.mail@google.com");
      cy.get("#NewUserPassword").type("random");
      cy.get("#NewUserConfirmPassword").type("random");
      cy.get("button").get("span").contains("Create").click({force:true}).wait(200);
      cy.get(".User").its("length").should("equal", numUsers + 1);
    });
  });
});

context('Manage tasks Administrator', () => {
  beforeEach(() => {
    cy.visit('http://localhost:3000/login');
    cy.get('#normal_login_username')
      .type('admin@admin.com');
    cy.get('#normal_login_password')
      .type('admin');
    cy.contains('Log in').click();
  });

  it('creates task', () => {
    cy.get(".Task").its("length").then(numTasks => {
      cy.get('.anticon-plus').click();
      cy.get('#createTask').should("be.visible");
      cy.get("#NewTitleTask").type("This is a task");
      cy.get(".ant-select-selection").click();
      cy.contains("admin").click();
      cy.get("button").get("span").contains("Create").click({force:true}).wait(200);
      cy.get(".Task").its("length").should("equal", numTasks + 1);
    });
  });

  it('creates task for user', () => {
    cy.get(".Task").its("length").then(numTasks => {
      cy.get('.anticon-plus').click();
      cy.get('#createTask').should("be.visible");
      cy.get("#NewTitleTask").type("This is a task");
      cy.get(".ant-select-selection").click();
      cy.contains("random").click();
      cy.get("button").get("span").contains("Create").click({force:true}).wait(200);
      cy.get(".Task").its("length").should("equal", numTasks + 1);
    });
  });

  it('delete task', () => {
    cy.get(".Task").its("length").then(numTasks => {
      cy.get('.anticon-close').first().click({force: true}).wait(1000);
      cy.get(".Task").its("length").should("equal", numTasks - 1);
    });
  });
});

context('Manage tasks User', () => {
  beforeEach(() => {
    cy.visit('http://localhost:3000/login');
    cy.get('#normal_login_username')
      .type('random.mail@google.com');
    cy.get('#normal_login_password')
      .type('random');
    cy.contains('Log in').click();
  });

  it('.creates task', () => {
    cy.get(".Task").its("length").then(numTasks => {
      cy.get('.anticon-plus').click();
      cy.get('#createTask').should("be.visible");
      cy.get("#NewTitleTask").type("This is a task");
      cy.get("button").get("span").contains("Create").click({force:true}).wait(200);
      cy.get(".Task").its("length").should("equal", numTasks + 1);
    });
  });
});