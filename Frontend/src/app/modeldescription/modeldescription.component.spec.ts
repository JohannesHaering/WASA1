import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModeldescriptionComponent } from './modeldescription.component';

describe('ModeldescriptionComponent', () => {
  let component: ModeldescriptionComponent;
  let fixture: ComponentFixture<ModeldescriptionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ModeldescriptionComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ModeldescriptionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
