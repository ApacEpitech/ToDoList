context('Actions', () => {
  beforeEach(() => {
    cy.visit('http://localhost:3000/login')
  });

  it('.fail to connect', () => {
    cy.get('#normal_login_username')
      .type('fake@email.com').should('have.value', 'fake@email.com');

    cy.get('#normal_login_password')
      .type('fake');
    cy.contains('Log in').click();
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
    cy.url().should('include', '/homeAdmin?show=All')
  });
});
