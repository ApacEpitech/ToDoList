context('Connect', () => {
  beforeEach(() => {
    cy.visit('http://localhost:3000/login')
  });
  it('.fail to connect', () => {
    cy.get('#normal_login_username')
      .type('fake@email.com').should('have.value', 'fake@email.com');

    cy.get('#normal_login_password')
      .type('fake');
    cy.contains('Log in').click().wait(1000);
    cy.on('window:alert', (str) => {
        expect(str).to.equal(`Email Or Password Incorrect`)
    });
  });
  it('.success to connect', () => {
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

context('Manage tasks Administrator', () => {
  beforeEach(() => {
    cy.visit('http://localhost:3000/login');
    cy.get('#normal_login_username')
      .type('admin@admin.com');
    cy.get('#normal_login_password')
      .type('admin');
    cy.contains('Log in').click();
  });

  it('.creates task', () => {
    cy.get(".Task").its("length").then(numTasks => {
      cy.get('.anticon-plus').click();
      cy.get('#createTask').should("be.visible");
      cy.get("#NewTitleTask").type("This is a task");
      cy.get(".ant-select-selection").click();
      cy.contains("admin").click();
      cy.get("button").get("span").contains("Create").click({force:true});
      cy.get(".Task").its("length").should("equal", numTasks + 1);
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
      cy.get(".ant-select-selection").click();
      cy.get("button").get("span").contains("Create").click({force:true});
      cy.get(".Task").its("length").should("equal", numTasks + 1);
    });
  });
});