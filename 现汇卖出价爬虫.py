import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, WebDriverException

if __name__ == '__main__':
    # 创建Chrome浏览器的无头选项
    chrome_options = Options()
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36")
    # 设置页面加载策略为“eager”，即仅等待DOM加载完成
    chrome_options.page_load_strategy = 'eager'
    # 添加一些选项来绕过网站对Selenium的检测
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("prefs", {"javascript.enabled": False})
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    try:
        # 尝试从Excel文件中读取数据
        df = pd.read_excel('货币符号与中文转换.xlsx')
    except FileNotFoundError:
        print("未找到Excel文件，请检查文件路径。")
        exit()

    date = input('请输入您想要查询的日期：')
    if len(date) != 8:
        print('日期格式错误！请输入正确的日期格式，如20230205')
        exit()
    else:
        if float(date[:4]) > 2024 or float(date[:4]) < 2001:
            print('您输入的日期超出查询范围！可查询范围为2001年至2024年')
            exit()
    currency_input = input('请输入您想要查询的货币：')
    # 查找并输出符合条件的货币中文名称
    result = df.loc[df['货币标准符号'] == currency_input, '货币中文'].values
    if len(result) > 0:
        currency = result[0]
    else:
        print("未找到匹配的货币符号，请检查输入。")
        exit()

    url = 'https://www.boc.cn/sourcedb/whpj/'

    try:
        # 初始化webdriver
        driver = webdriver.Chrome(options=chrome_options)
        # 进一步将webdriver隐藏，使其无法被检测
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.get(url)
    except WebDriverException:
        print("WebDriver初始化失败，请检查您的ChromeDriver是否正确安装和配置。")
        exit()

    try:
        # 查找并操作页面元素
        search_bar = driver.find_element(By.XPATH, '//*[@id="nothing"]')  # 时间输入框
        search_bar.send_keys(date)  # 输入期望时间
        select_element = driver.find_element(By.XPATH, "//select[@id='pjname']")  # 货币下拉框
        select = Select(select_element)  # 使用 Select 对象包装下拉框元素
        select.select_by_visible_text(f"{currency}")  # 通过货币中文名称选择下拉选项
        button = driver.find_element(By.XPATH, "/html/body/div/div[5]/div[1]/div[2]/div/form/div/table/tbody/tr/td[7]/input")  # 搜索按钮
        button.click()  # 点击搜索按钮
        spot_selling_price = driver.find_element(By.XPATH, '/html/body/div/div[4]/table/tbody/tr[2]/td[4]').text  # 搜索结果页查找第一行的现汇卖出价
        print(f'您好，您所查询的现汇卖出价为：{spot_selling_price}')
        # 将数据写入到文件中
        with open("../result.txt", "w") as file:
            file.write(spot_selling_price)
    except NoSuchElementException:
        print("未能找到页面上的某些元素，请确保页面结构没有变化。")
    finally:
        driver.quit()  # 无论成功与否，最后都关闭浏览器
