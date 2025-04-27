import React from 'react';
import { useNavigate } from 'react-router-dom'; // React Router 的用法
import './AboutPage.css'; // 样式文件 (可以根据需要添加)
import { TypeAnimation } from 'react-type-animation';
import SplashCursor from './SplashCursor';

const AboutPage = () => {
  const navigate = useNavigate();

  const handleGetStartedClick = () => {
    navigate('/function'); // 这里跳转到功能页面
  };

  return (
    <div className="about-page-container">
      <SplashCursor />
      <div className="about-header">
        <TypeAnimation
          sequence={[
            'Welcome to Smart Chef',
          ]}
          wrapper="span"
          speed={50}
          style={{ fontSize: '3em', display: 'inline-block', fontWeight: 'bold' }}
          repeat={0}
        />
        <p className="about-subtitle">Your personal AI-powered chef</p>
      </div>

      <div className="about-content">
        <div className="about-text">
          <p>Smart Chef is an AI-powered application that generates personalized recipes based on the ingredients you have at hand. No more guesswork in the kitchen — just input your ingredients and let Smart Chef do the magic!</p>
          <p>It not only gives you the best recipes but also provides images of the dishes to inspire you. Whether you're cooking for yourself or entertaining guests, Smart Chef has you covered!</p>
        </div>
      </div>

      <div className="about-footer">
        <button
          onClick={handleGetStartedClick}
          className="btn btn-primary"
        >
          Get Started
        </button>
      </div>
    </div>
  );
};

export default AboutPage;
