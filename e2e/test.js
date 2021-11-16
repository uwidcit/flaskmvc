const puppeteer = require('puppeteer');
const { expect, assert }  = require('chai');
const config = require('./config.json');

let browser;
let page;
let requests = [];

const host = 'http://localhost:8080';

before(async function(){
  this.timeout(config.timeout);
  browser = await puppeteer.launch(config);
  [page] = await browser.pages();

  await page.emulateMediaType("screen");
  await page.setRequestInterception(true);

  page.on('request', request => {
    requests.push(request.url());
    request.continue();
  });

  await page.goto(`${host}/static/users`, { waitUntil: 'networkidle2'});
});

function getHTML(selector){
  return page.evaluate(selector=>{
    try{
      return document.querySelector(selector).outerHTML;
    }catch(e){
      return null;
    }
  }, selector);
}

function getInnerText(a) {
  return page.evaluate(a => document.querySelector(a).innerText, a)
}

function checkElements(a) {
  for (let [b, c] of Object.entries(a)) it(`Should have ${b}`, async () => {
      expect(await page.$(c)).to.be.ok
  })
}

context('The /static/users page', ()=>{

  it('Test 1: Should send a http request to /api/users', async ()=>{
    let reqs = [
      `${host}/api/users`,
    ];

    let count = 0;

    reqs.forEach(req => {
      if(requests.includes(req))count++
    })

    expect(count).to.equal(reqs.length);

  }).timeout(2000);

  it("Test 2: Page should have App Users as the title", async () => {
      expect(await page.title()).to.eql("App Users");
  });

  // describe("Test 3: Page should have a users table with the appropriate structure", () => {
  //   it("First table header should be 'Id'", async () => {
  //     const html = await page.$eval('tr>th:nth-child(1)', (e) => e.innerHTML);
  //     expect(html).to.eql("Id");
  //   });

  //   it("Second table header should be 'First Name'", async () => {
  //     const html = await page.$eval('tr>th:nth-child(2)', (e) => e.innerHTML);
  //     expect(html).to.eql("First Name");
  //   });

  //   it("Third table header should be 'Last Name'", async () => {
  //     const html = await page.$eval('tr>th:nth-child(3)', (e) => e.innerHTML);
  //     expect(html).to.eql("Last Name");
  //   });

  // })

  // it('Test 2: Should user table header on page', async ()=>{
  //   await page.waitForSelector('#pokemon-detail')

  //   let searchKeys = [ 'grass', '1', '6.9', '0.7' ]

  //   let result = await getHTML('#pokemon-detail');

  //   let count = 0;

  //   for(let key of searchKeys){
  //     if(result.includes(key))count++
  //   }

  //   expect(count).to.eql(4);
      
  // }).timeout(2000);

  it('Test 7: Delete button reduces the amount of rows in the table', async ()=>{

    await page.goto('https://snick-flask-sample.herokuapp.com/app1');
    
    await page.waitForSelector('.table > tbody > tr:nth-child(1) > td > .btn');

    const rowCountBefore = await page.$$eval('body > .container > .row  tr', (divs) => divs.length);
    await page.click('.table > tbody > tr:nth-child(1) > td > .btn');

    const rowCountAfter = await page.$$eval('body > .container > .row  tr', (divs) => divs.length);
    
    assert(rowCountBefore > rowCountAfter, 'Num rows mush be reduced');
  });
      

});



after(async () => {
  await browser.close();
});



