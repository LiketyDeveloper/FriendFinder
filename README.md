<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/LiketyDeveloper/FriendFinder">
    <img src="static\FriendFinder.jpg" height=400>
  </a>

<h3 align="center">FriendFinder</h3>

  <p align="center">
    People you've been searching for,
    <br /> But haven't found yet
    <br />
    <br />
    <a href="https://github.com/LiketyDeveloper/FriendFinder"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/LiketyDeveloper/FriendFinder/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/LiketyDeveloper/FriendFinder/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<img src="static\screenshot.png" height=400 style="border: 3px solid;border-radius: 20px;">

This Telegram bot is designed to help users find new friends based on their shared interests. 
<br /> It enables them to connect with like-minded people and engage in conversations about topics that are meaningful to them.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With
* [![Telebot][Telebot]][Telebot-url]
* [![PostgreSQL][PostgreSQL]][PostgreSQL-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

That's how you can start this bot by yourself on your own computer

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.

* Download the [Python](https://www.python.org/downloads/)
* Upgrade packet manager `pip`
  ```sh
  python -m pip install --upgrade pip
  ```
* Download [PgAdmin](https://www.pgadmin.org/download/)

### Installation

1. Get a free API Key from [Bot Father](https://web.telegram.org/a/#93372553) in Telegram
2. Clone the repo
   ```sh
   git clone https://github.com/LiketyDeveloper/FriendFinder.git
   ```
3. Install all required packages
   ```sh
   pip install -r requirements.txt
   ```
4. Enter your API and database credentials in `config.py`
   ```python
   TG_API_KEY = "YOUR_API_KEY"

   DATABASE_NAME = "YOUR_DB_NAME"
   USERNAME = "YOUR_DB_USERNAME"
   PASSWORD = "YOUR_DB_PASSWORD"
   DB_HOST = "YOUR_DB_HOST"
   ```
5. Change git remote url to avoid accidental pushes to base project
   ```sh
   git remote set-url origin github_username/repo_name
   git remote -v # confirm the changes
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

To run the bot, use the following command in your terminal:
```Python
python main.py
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- **Profiles and profile management**:
    - Set your `profile photo`, `username`, `description`, and `interests`.
- **Explore user feeds**: Find the person you're looking for!
- **Accept or deny friend requests**: It's up to you!
- **Chat with friends**: No need to share your contacts. But if you want to, you can share your contacts and chat beyond the bot!


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:

<a href="https://github.com/LiketyDeveloper/FriendFinder/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=LiketyDeveloper/FriendFinder" alt="contrib.rocks image" />
</a>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Ivan Skrebtsoff <br />
My e-mail - ivanscrebtsoff@gmail.com

Project Link: [https://github.com/LiketyDeveloper/FriendFinder](https://github.com/LiketyDeveloper/FriendFinder)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/LiketyDeveloper/FriendFinder.svg?style=for-the-badge
[contributors-url]: https://github.com/LiketyDeveloper/FriendFinder/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/LiketyDeveloper/FriendFinder.svg?style=for-the-badge
[forks-url]: https://github.com/LiketyDeveloper/FriendFinder/network/members
[stars-shield]: https://img.shields.io/github/stars/LiketyDeveloper/FriendFinder.svg?style=for-the-badge
[stars-url]: https://github.com/LiketyDeveloper/FriendFinder/stargazers
[issues-shield]: https://img.shields.io/github/issues/LiketyDeveloper/FriendFinder.svg?style=for-the-badge
[issues-url]: https://github.com/LiketyDeveloper/FriendFinder/issues
[license-shield]: https://img.shields.io/github/license/LiketyDeveloper/FriendFinder.svg?style=for-the-badge
[license-url]: https://github.com/LiketyDeveloper/FriendFinder/blob/master/LICENSE.txt

[Telebot]: https://img.shields.io/badge/Telebot-000000?style=for-the-badge&logo=telegram&logoColor=white
[Telebot-url]: https://pytba.readthedocs.io/en/latest
[PostgreSQL]: https://img.shields.io/badge/PostgreSQL-000000?style=for-the-badge&logo=postgresql&logoColor=white
[PostgreSQL-url]: https://www.postgresql.org/
