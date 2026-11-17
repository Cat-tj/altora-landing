(()=>{
  const overlay=document.querySelector('[data-ticket-overlay]');
  const form=document.querySelector('[data-ticket-form]');
  if(!form)return;

  const isIndonesian=document.documentElement.lang.toLowerCase().startsWith('id');
  const copy=isIndonesian?{
    sending:'Mengirim tiket…',submit:'Kirim kebutuhan & buat tiket →',
    generic:'Periksa kembali isian yang diberi tanda merah, lalu kirim ulang.',
    required:(label)=>`Tolong isi ${label}.`,
    email:'Masukkan alamat email yang valid, misalnya nama@email.com.',
    min:(label,count)=>`${label} masih terlalu singkat. Tambahkan ${count} karakter lagi (minimal 15 karakter).`,
    success:(ticket)=>`Tiket ${ticket} berhasil dibuat. Konfirmasi sudah dikirim ke email Anda.`,
    remaining:(count)=>`${count} karakter lagi agar konteksnya cukup jelas.`,
    ready:'Konteks sudah cukup jelas untuk dikirim.',
    invalidServer:'Tiket belum dapat dibuat. Periksa isian lalu coba lagi.',
  }:{
    sending:'Sending ticket…',submit:'Send need & make ticket →',
    generic:'Please check the fields marked in red, then submit again.',
    required:(label)=>`Please complete ${label}.`,
    email:'Enter a valid email address, for example name@email.com.',
    min:(label,count)=>`${label} is too short. Add ${count} more characters (minimum 15 characters).`,
    success:(ticket)=>`Ticket ${ticket} has been created. A confirmation was sent to your email.`,
    remaining:(count)=>`${count} more characters will make the context clear enough.`,
    ready:'The context is clear enough to send.',
    invalidServer:'The ticket could not be created. Check the details and try again.',
  };

  const fields=[
    {name:'name',label:isIndonesian?'nama':'your name',min:2},
    {name:'email',label:'email',email:true},
    {name:'whatsapp',label:isIndonesian?'nomor WhatsApp':'WhatsApp number',min:8},
    {name:'city',label:isIndonesian?'kota atau daerah':'city or area',min:2},
    {name:'service',label:isIndonesian?'kebutuhan layanan':'service need'},
    {name:'needs',label:isIndonesian?'kondisi atau proses yang ingin dirapikan':'operational challenge or process to improve',min:15},
  ];
  const out=form.querySelector('[data-ticket-result]');
  const btn=form.querySelector('button[type="submit"]');
  const needs=form.elements.needs;
  const counter=form.querySelector('[data-needs-counter]');

  // Tanpa overlay (form tampil langsung di halaman), tombol pembuka cukup menggulir ke form.
  const open=()=>{if(!overlay){form.scrollIntoView({behavior:'smooth',block:'start'});setTimeout(()=>form.elements.name.focus({preventScroll:true}),400);return}overlay.hidden=false;document.body.style.overflow='hidden';setTimeout(()=>form.elements.name.focus(),50)};
  const close=()=>{if(!overlay)return;overlay.hidden=true;document.body.style.overflow=''};
  document.querySelectorAll('[data-ticket-open]').forEach(button=>button.addEventListener('click',open));
  document.querySelectorAll('[data-ticket-close]').forEach(button=>button.addEventListener('click',close));
  if(overlay){
    overlay.addEventListener('click',event=>{if(event.target===overlay)close()});
    document.addEventListener('keydown',event=>{if(event.key==='Escape'&&!overlay.hidden)close()});
  }

  function fieldErrorElement(input){
    const label=input.closest('label');
    let error=label.querySelector('[data-field-error]');
    if(!error){
      error=document.createElement('span');
      error.className='field-error';
      error.dataset.fieldError='';
      error.setAttribute('role','alert');
      label.append(error);
    }
    return error;
  }

  function clearFieldError(input){
    input.removeAttribute('aria-invalid');
    const error=input.closest('label')?.querySelector('[data-field-error]');
    if(error)error.textContent='';
  }

  function showFieldError(input,message){
    input.setAttribute('aria-invalid','true');
    fieldErrorElement(input).textContent=message;
  }

  function validateField(field){
    const input=form.elements[field.name];
    const value=String(input.value||'').trim();
    let message='';
    if(!value)message=copy.required(field.label);
    else if(field.email&&!input.validity.valid)message=copy.email;
    else if(field.min&&value.length<field.min)message=copy.min(field.label,field.min-value.length);
    if(message)showFieldError(input,message);else clearFieldError(input);
    return !message;
  }

  function updateNeedsCounter(){
    if(!needs||!counter)return;
    const remaining=Math.max(0,15-String(needs.value||'').trim().length);
    counter.textContent=remaining?copy.remaining(remaining):copy.ready;
    counter.classList.toggle('ready',remaining===0);
  }

  fields.forEach(field=>{
    const input=form.elements[field.name];
    input.addEventListener('input',()=>{if(input.getAttribute('aria-invalid')==='true')validateField(field);if(field.name==='needs')updateNeedsCounter()});
    input.addEventListener('change',()=>validateField(field));
    input.addEventListener('blur',()=>validateField(field));
  });
  updateNeedsCounter();

  form.addEventListener('submit',async event=>{
    event.preventDefault();
    out.className='form-result';
    out.textContent='';
    const invalid=fields.filter(field=>!validateField(field));
    if(invalid.length){
      out.className='form-result error';
      out.textContent=copy.generic;
      form.elements[invalid[0].name].focus();
      return;
    }
    btn.disabled=true;
    btn.textContent=copy.sending;
    try{
      const response=await fetch('/api/tickets',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(Object.fromEntries(new FormData(form)))});
      const data=await response.json().catch(()=>({}));
      if(!response.ok)throw new Error(data.error||copy.invalidServer);
      out.className='form-result success';
      out.textContent=copy.success(data.ticket);
      form.reset();
      fields.forEach(field=>clearFieldError(form.elements[field.name]));
      updateNeedsCounter();
    }catch(error){
      out.className='form-result error';
      out.textContent=error.message||copy.invalidServer;
    }finally{
      btn.disabled=false;
      btn.textContent=copy.submit;
    }
  });
})();
