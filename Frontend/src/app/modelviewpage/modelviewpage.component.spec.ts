import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModelviewpageComponent } from './modelviewpage.component';

describe('ModelviewpageComponent', () => {
  let component: ModelviewpageComponent;
  let fixture: ComponentFixture<ModelviewpageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ModelviewpageComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ModelviewpageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
