const fs = require('fs');
const cheerio = require('cheerio');

const mapping = {
  "dependent-visa": {
    "title": "Dependent Visa",
    "breadcrumb": "Dependent Visa",
    "main_text": "EDU2EXCEL can also assist with dependent visa applications for family members of primary visa holders, such as student or work visa holders. Their services include:",
    "list_items": [
      "Eligibility Assessment: Determining whether you meet the eligibility criteria for a dependent visa based on your relationship and the primary visa holder's status.",
      "Documentation Support: Helping you gather the necessary documents, such as proof of relationship, financial support, and health insurance.",
      "Application Assistance: Guiding you through the application process, ensuring that all forms are completed accurately and on time.",
      "Interview Preparation: Providing tips and practice questions to help you prepare for your visa interview.",
      "Post-Arrival Support: Offering assistance with settling in the new country, finding accommodation, and accessing essential services."
    ],
    "why_choose_title": "WHY CHOOSE EDU2EXCEL",
    "why_choose_subtitle": "Benefits of Choosing EDU2EXCEL",
    "why_choose_text": "By choosing EDU2EXCEL for your dependent visa application, you can benefit from their expertise, personalized guidance, and commitment to ensuring a successful outcome.<br><br>Would you like to know more about EDU2EXCEL's services for dependent visas or have any specific questions?"
  },
  "work-permit": {
    "title": "Work Permit",
    "breadcrumb": "Work Permit",
    "main_text": "EDU2EXCEL can also assist with work visa applications for individuals seeking employment in a foreign country. Their services include:",
    "list_items": [
      "Job Search Assistance: Helping you find suitable job opportunities in your desired field and location.",
      "Resume and Cover Letter Preparation: Assisting you in crafting compelling resumes and cover letters that highlight your skills and experience.",
      "Visa Application Support: Guiding you through the work visa application process, ensuring that all required documents are submitted on time.",
      "Interview Preparation: Providing tips and practice questions to help you prepare for your work visa interview.",
      "Post-Arrival Support: Offering assistance with finding accommodation, opening a bank account, and adapting to the workplace culture."
    ],
    "why_choose_title": "WHY CHOOSE EDU2EXCEL",
    "why_choose_subtitle": "Benefits of Choosing EDU2EXCEL",
    "why_choose_text": "By choosing EDU2EXCEL for your work visa application, you can benefit from their expertise, personalized guidance, and commitment to ensuring a successful outcome.<br><br>Would you like to know more about EDU2EXCEL's services for work visas or have any specific questions?"
  },
  "pr-visa": {
    "title": "PR Visa",
    "breadcrumb": "PR Visa",
    "main_text": "EDU2EXCEL can also assist with permanent residency (PR) visa applications for individuals seeking to live and work permanently in a foreign country. Their services include:",
    "list_items": [
      "Eligibility Assessment: Determining your eligibility for different PR visa categories based on your qualifications, work experience, and other criteria.",
      "Documentation Support: Helping you gather and prepare the necessary documents, such as proof of identity, education, employment, and language proficiency.",
      "Application Assistance: Guiding you through the PR visa application process, ensuring that all forms are completed accurately and on time.",
      "Interview Preparation: Providing tips and practice questions to help you prepare for your PR visa interview.",
      "Post-Arrival Support: Offering assistance with settling in the new country, finding accommodation, and accessing essential services."
    ],
    "why_choose_title": "WHY CHOOSE EDU2EXCEL",
    "why_choose_subtitle": "Benefits of Choosing EDU2EXCEL",
    "why_choose_text": "By choosing EDU2EXCEL for your PR visa application, you can benefit from their expertise, personalized guidance, and commitment to ensuring a successful outcome.<br><br>Would you like to know more about EDU2EXCEL's services for PR visas or have any specific questions?"
  },
  "visit-visa": {
    "title": "Visit Visa",
    "breadcrumb": "Visit Visa",
    "main_text": "While EDU2EXCEL primarily focuses on education and immigration services, they may also be able to provide some assistance with visit visa applications. While visit visas are generally straightforward to obtain, EDU2EXCEL can offer guidance and support, particularly for first-time travelers or those with complex travel plans. They can help with:",
    "list_items": [
      "Understanding Visa Requirements: Providing information on the specific requirements for visit visas to your desired destination.",
      "Document Preparation: Assisting you in gathering the necessary documents, such as passport, proof of funds, and itinerary.",
      "Application Guidance: Offering advice on completing the visa application form and preparing for any interviews."
    ],
    "why_choose_title": "WHY CHOOSE EDU2EXCEL",
    "why_choose_subtitle": "Benefits of Choosing EDU2EXCEL",
    "why_choose_text": "It's important to note that EDU2EXCEL may not have the same level of expertise in visit visas as they do in education and immigration matters. However, they can still provide valuable assistance and guidance, especially if you have any concerns or questions.<br><br>Would you like to know more about EDU2EXCEL's services or have any specific questions about visit visas?"
  }
};

async function run() {
  for (const [folder, data] of Object.entries(mapping)) {
    const filePath = `services/${folder}/index.html`;
    if (!fs.existsSync(filePath)) {
      console.log(`Skipping ${filePath}, does not exist.`);
      continue;
    }
    const html = fs.readFileSync(filePath, 'utf8');
    const $ = cheerio.load(html, { decodeEntities: false });

    // Update <title>
    const titleEl = $('title');
    if (titleEl.length > 0) {
      titleEl.text(`${data.title} - EDU2EXCEL`);
    }

    // Update h1 elementor-heading-title
    const h1 = $('h1.elementor-heading-title');
    if (h1.length > 0) {
      h1.text(data.title);
    }

    // Update breadcrumb
    // It's usually inside a <div class="breadcumb"> or similar, but we can find it by looking for the last <li> 
    // or an <li> that does not have an <a> tag
    $('li').each((i, el) => {
      const text = $(el).text().trim().toLowerCase();
      // the old names might be family visa, working visa, etc.
      if (['family visa', 'working visa', 'residency visa', 'tourists visa', 'tourist visa'].includes(text)) {
        $(el).text(data.breadcrumb);
      }
    });

    // Update the main paragraph: <p>Navigating the visa application process can be overwhelming...</p>
    // We can find the container by data-id="366aed4" or just searching for the paragraph text
    $('p').each((i, el) => {
      const text = $(el).text().trim();
      if (text.includes("Navigating the visa application process") || text.includes("EDU2EXCEL") || text.includes("Working visa process")) {
        $(el).text(data.main_text);
      }
    });
    // For specific cases like Tourists Visa, old text might be different. 
    // Wait, let's just use data-id="366aed4" which is the text-editor container
    const mainTextContainer = $('[data-id="366aed4"] .elementor-widget-container');
    if (mainTextContainer.length > 0) {
      mainTextContainer.html(`<p>${data.main_text}</p>`);
    }

    // Update the list items
    // The list we want to update is in data-id="7fe3374"
    const listContainer = $('[data-id="7fe3374"] ul.elementor-icon-list-items');
    if (listContainer.length > 0) {
      // Create new list items based on the first item's HTML structure
      const firstItemHTML = listContainer.find('li').first().html();
      listContainer.empty();
      
      data.list_items.forEach(itemText => {
        // We will create a new <li> element
        const newLi = $('<li class="elementor-icon-list-item"></li>');
        newLi.html(firstItemHTML);
        // Replace the text inside .elementor-icon-list-text
        newLi.find('.elementor-icon-list-text').text(itemText);
        listContainer.append(newLi);
      });
    }

    // Update "WHY CHOOSE IMIGO" -> "WHY CHOOSE EDU2EXCEL"
    // Usually data-id="983726c"
    const whyChooseH3 = $('[data-id="983726c"] h3');
    if (whyChooseH3.length > 0) {
      whyChooseH3.text(data.why_choose_title);
    }

    // Update "Countless benefits & easy processing"
    // Usually data-id="bfce2f7"
    const whyChooseSubH2 = $('[data-id="bfce2f7"] h2');
    if (whyChooseSubH2.length > 0) {
      whyChooseSubH2.text(data.why_choose_subtitle);
    }

    // Update the paragraph below "Countless benefits"
    // Usually data-id="95958fa"
    const whyChooseTextContainer = $('[data-id="95958fa"] .elementor-widget-container');
    if (whyChooseTextContainer.length > 0) {
      whyChooseTextContainer.html(`<p>${data.why_choose_text}</p>`);
    }
    
    // Also update any sidebar links to point to the new URLs
    $('a').each((i, el) => {
      const href = $(el).attr('href');
      if (href) {
        let newHref = href;
        newHref = newHref.replace('family-visa', 'dependent-visa');
        newHref = newHref.replace('working-visa', 'work-permit');
        newHref = newHref.replace('residency-visa', 'pr-visa');
        newHref = newHref.replace('tourists-visa', 'visit-visa');
        if (newHref !== href) {
          $(el).attr('href', newHref);
        }
      }
    });
    
    // Also update the sidebar text for the links
    $('.service-catagery-list .elementor-icon-list-text').each((i, el) => {
      const text = $(el).text().trim();
      if (text === 'Family Visa') $(el).text('Dependent Visa');
      if (text === 'Working Visa') $(el).text('Work Permit');
      if (text === 'Residency Visa') $(el).text('PR Visa');
      if (text === 'Tourists Visa') $(el).text('Visit Visa');
    });

    fs.writeFileSync(filePath, $.html());
    console.log(`Updated ${filePath}`);
  }
}

run();
