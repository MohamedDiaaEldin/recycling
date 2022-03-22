


export const get_day = ()=>{
    const today_date = new Date()
    return String(today_date.getDate()).padStart(2, '0')
}   

export const get_month = ()=>{
    const today_date = new Date()
    return  String(today_date.getMonth() + 1).padStart(2, '0');
}   
export const get_year = ()=>{
    return new Date().getFullYear()
}
